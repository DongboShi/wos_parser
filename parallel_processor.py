#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Concurrent file processing capabilities for WOS data
"""

from concurrent.futures import ProcessPoolExecutor, as_completed
import os
from typing import Callable, List, Dict, Tuple


class ParallelFileProcessor:
    """Handles concurrent processing of WOS data files"""
    
    def __init__(self, worker_count=None):
        if worker_count is None:
            worker_count = os.cpu_count() or 1
        self.worker_count = worker_count
        self.stats = {'processed': 0, 'errors': 0}
        
    def scan_directory_tree(self, root_path: str) -> List[str]:
        """Recursively find all processable files"""
        found_files = []
        
        try:
            entries = os.listdir(root_path)
        except (PermissionError, FileNotFoundError):
            return found_files
            
        for entry in entries:
            full_path = os.path.join(root_path, entry)
            
            if os.path.isdir(full_path):
                found_files.extend(self.scan_directory_tree(full_path))
            elif not entry.startswith('.'):
                found_files.append(full_path)
                
        return found_files
    
    def execute_on_file(self, filepath: str, handler: Callable) -> Tuple[bool, str, str]:
        """Execute processing handler on a single file"""
        try:
            from paper_info_load_api import load_paper_info_file
            load_paper_info_file(filepath, handler)
            return (True, filepath, "")
        except Exception as err:
            return (False, filepath, str(err))
    
    def run_batch(self, handler: Callable, input_directory: str) -> Dict:
        """Execute batch processing with concurrent workers"""
        target_path = os.path.join(os.getcwd(), input_directory)
        
        print(f"Scanning: {target_path}")
        file_list = self.scan_directory_tree(target_path)
        total_count = len(file_list)
        
        if total_count == 0:
            return {'total': 0, 'ok': 0, 'failed': 0, 'failures': []}
        
        print(f"Located {total_count} files for processing")
        
        actual_workers = min(self.worker_count, total_count)
        print(f"Launching {actual_workers} concurrent workers")
        
        outcomes = {'total': total_count, 'ok': 0, 'failed': 0, 'failures': []}
        completed = 0
        
        with ProcessPoolExecutor(max_workers=actual_workers) as executor:
            task_map = {
                executor.submit(self.execute_on_file, fpath, handler): fpath 
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


def process_with_concurrency(handler: Callable, directory: str, workers=None):
    """Convenience function for concurrent processing"""
    processor = ParallelFileProcessor(worker_count=workers)
    return processor.run_batch(handler, directory)
