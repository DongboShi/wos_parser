#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Concurrent XML file processing capabilities for WOS XML data
"""

from concurrent.futures import ProcessPoolExecutor, as_completed
import os
from typing import Callable, List, Dict, Tuple


class XMLParallelFileProcessor:
    """Handles concurrent processing of WOS XML data files"""
    
    def __init__(self, worker_count=None):
        if worker_count is None:
            worker_count = os.cpu_count() or 1
        self.worker_count = worker_count
        
    def scan_directory_tree(self, root_path: str) -> List[str]:
        """Recursively find all XML files"""
        found_files = []
        
        try:
            entries = os.listdir(root_path)
        except (PermissionError, FileNotFoundError):
            return found_files
            
        for entry in entries:
            full_path = os.path.join(root_path, entry)
            
            if os.path.isdir(full_path):
                found_files.extend(self.scan_directory_tree(full_path))
            elif entry.endswith('.xml') and not entry.startswith('.'):
                found_files.append(full_path)
                
        return found_files
    
    def execute_on_file(self, filepath: str, handler: Callable, skip_processed: bool) -> Tuple[bool, str, str]:
        """Execute processing handler on a single XML file"""
        try:
            from xml_info_load_api import load_xml_file
            from xml_processing_history import ProcessingHistoryManager
            
            # Create a history manager for this worker
            history_manager = ProcessingHistoryManager()
            
            # Process the file with the handler
            load_xml_file(filepath, handler, skip_processed, history_manager)
            return (True, filepath, "")
        except Exception as err:
            return (False, filepath, str(err))
    
    def run_batch(self, handler: Callable, input_directory: str, skip_processed: bool = True) -> Dict:
        """Execute batch processing with concurrent workers"""
        target_path = os.path.join(os.getcwd(), input_directory) if not os.path.isabs(input_directory) else input_directory
        
        print(f"Scanning: {target_path}")
        file_list = self.scan_directory_tree(target_path)
        total_count = len(file_list)
        
        if total_count == 0:
            return {'total': 0, 'ok': 0, 'failed': 0, 'failures': []}
        
        print(f"Located {total_count} XML files for processing")
        
        # For very small file counts, sequential processing is more efficient
        if total_count < 3:
            print("File count is small, using sequential processing")
            return self._sequential_batch(handler, file_list, total_count, skip_processed)
        
        actual_workers = min(self.worker_count, total_count)
        print(f"Launching {actual_workers} concurrent workers")
        
        outcomes = {'total': total_count, 'ok': 0, 'failed': 0, 'failures': []}
        completed = 0
        
        with ProcessPoolExecutor(max_workers=actual_workers) as executor:
            task_map = {
                executor.submit(self.execute_on_file, fpath, handler, skip_processed): fpath 
                for fpath in file_list
            }
            
            for future in as_completed(task_map):
                completed += 1
                success, path, error_info = future.result()
                
                if success:
                    outcomes['ok'] += 1
                    print(f"[{completed}/{total_count}] OK: {os.path.basename(path)}")
                else:
                    outcomes['failed'] += 1
                    outcomes['failures'].append((path, error_info))
                    print(f"[{completed}/{total_count}] ERROR: {os.path.basename(path)}")
        
        self._print_summary(outcomes)
        return outcomes
    
    def _sequential_batch(self, handler: Callable, file_list: List[str], total_count: int, skip_processed: bool) -> Dict:
        """Execute batch processing sequentially for small file counts"""
        outcomes = {'total': total_count, 'ok': 0, 'failed': 0, 'failures': []}
        
        for i, fpath in enumerate(file_list, 1):
            success, path, error_info = self.execute_on_file(fpath, handler, skip_processed)
            
            if success:
                outcomes['ok'] += 1
                print(f"[{i}/{total_count}] OK: {os.path.basename(path)}")
            else:
                outcomes['failed'] += 1
                outcomes['failures'].append((path, error_info))
                print(f"[{i}/{total_count}] ERROR: {os.path.basename(path)}")
        
        self._print_summary(outcomes)
        return outcomes
    
    def _print_summary(self, outcomes: Dict):
        """Display processing summary"""
        print("\n" + "=" * 70)
        print("Processing Summary")
        print(f"  Total: {outcomes['total']}")
        print(f"  Success: {outcomes['ok']}")  
        print(f"  Errors: {outcomes['failed']}")
        print("=" * 70)
        
        if outcomes['failed'] > 0:
            print("\nFailed files:")
            for path, err in outcomes['failures']:
                print(f"  {os.path.basename(path)}: {err[:100]}")


def process_xml_with_concurrency(handler: Callable, directory: str, workers=None, skip_processed=True):
    """Convenience function for concurrent XML processing"""
    processor = XMLParallelFileProcessor(worker_count=workers)
    return processor.run_batch(handler, directory, skip_processed)
