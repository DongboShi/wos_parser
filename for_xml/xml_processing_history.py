"""
Processing History Manager

This module tracks which XML records have been processed to enable
incremental processing and avoid reprocessing the same records.
"""

import os
import json
from datetime import datetime


class ProcessingHistoryManager:
    """Manages processing history to skip already processed records"""
    
    def __init__(self, history_file="processing_history.json"):
        """
        Initialize the processing history manager
        
        :param history_file: Path to the JSON file storing processing history
        """
        self.history_file = history_file
        self.history = self._load_history()
    
    def _load_history(self):
        """Load processing history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load history file: {e}")
                return self._create_empty_history()
        else:
            return self._create_empty_history()
    
    def _create_empty_history(self):
        """Create empty history structure"""
        return {
            "metadata": {
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "version": "1.0"
            },
            "processed_records": {},
            "processed_files": {},
            "statistics": {
                "total_records": 0,
                "total_files": 0,
                "total_errors": 0
            }
        }
    
    def _save_history(self):
        """Save processing history to file"""
        try:
            self.history["metadata"]["last_updated"] = datetime.now().isoformat()
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save history file: {e}")
    
    def is_record_processed(self, uid):
        """
        Check if a record has been processed
        
        :param uid: Record UID
        :return: True if record was already processed
        """
        return uid in self.history["processed_records"]
    
    def is_file_processed(self, file_path):
        """
        Check if a file has been fully processed
        
        :param file_path: Path to the XML file
        :return: True if file was already processed
        """
        # Get absolute path for consistency
        abs_path = os.path.abspath(file_path)
        return abs_path in self.history["processed_files"]
    
    def mark_record_processed(self, uid, file_path=None, metadata=None):
        """
        Mark a record as processed
        
        :param uid: Record UID
        :param file_path: Optional source file path
        :param metadata: Optional additional metadata
        """
        self.history["processed_records"][uid] = {
            "processed_at": datetime.now().isoformat(),
            "source_file": file_path,
            "metadata": metadata or {}
        }
        self.history["statistics"]["total_records"] += 1
        self._save_history()
    
    def mark_file_processed(self, file_path, record_count, error_count=0):
        """
        Mark a file as fully processed
        
        :param file_path: Path to the XML file
        :param record_count: Number of records in the file
        :param error_count: Number of errors encountered
        """
        abs_path = os.path.abspath(file_path)
        
        # Get file stats
        file_stats = os.stat(file_path)
        
        self.history["processed_files"][abs_path] = {
            "processed_at": datetime.now().isoformat(),
            "record_count": record_count,
            "error_count": error_count,
            "file_size": file_stats.st_size,
            "file_modified": datetime.fromtimestamp(file_stats.st_mtime).isoformat()
        }
        
        self.history["statistics"]["total_files"] += 1
        self.history["statistics"]["total_errors"] += error_count
        self._save_history()
    
    def mark_error(self, uid, error_message, file_path=None):
        """
        Record an error for a specific record
        
        :param uid: Record UID
        :param error_message: Error description
        :param file_path: Optional source file path
        """
        if uid not in self.history["processed_records"]:
            self.history["processed_records"][uid] = {}
        
        self.history["processed_records"][uid].update({
            "error": True,
            "error_message": error_message,
            "error_time": datetime.now().isoformat(),
            "source_file": file_path
        })
        
        self.history["statistics"]["total_errors"] += 1
        self._save_history()
    
    def get_processed_count(self):
        """Get total number of processed records"""
        return len(self.history["processed_records"])
    
    def get_file_count(self):
        """Get total number of processed files"""
        return len(self.history["processed_files"])
    
    def get_error_count(self):
        """Get total number of errors"""
        return self.history["statistics"]["total_errors"]
    
    def get_statistics(self):
        """Get processing statistics"""
        return {
            "total_records": len(self.history["processed_records"]),
            "total_files": len(self.history["processed_files"]),
            "total_errors": self.history["statistics"]["total_errors"],
            "last_updated": self.history["metadata"]["last_updated"]
        }
    
    def reset_history(self):
        """Clear all processing history"""
        confirm = input("Are you sure you want to reset all processing history? (yes/no): ")
        if confirm.lower() == "yes":
            self.history = self._create_empty_history()
            self._save_history()
            print("Processing history reset successfully")
        else:
            print("Reset cancelled")
    
    def get_record_info(self, uid):
        """Get information about a specific record
        
        :param uid: Record UID
        :return: Record information dict or None
        """
        return self.history["processed_records"].get(uid)

    
    def get_file_info(self, file_path):
        """
        Get information about a specific file
        
        :param file_path: Path to the XML file
        :return: File information dict or None
        """
        abs_path = os.path.abspath(file_path)
        return self.history["processed_files"].get(abs_path)
    
    def remove_record(self, uid):
        """Remove a record from processing history (to allow reprocessing)
        
        :param uid: Record UID
        """
        if uid in self.history["processed_records"]:
            del self.history["processed_records"][uid]
            self._save_history()
            print(f"Removed record {uid} from history")
        else:
            print(f"Record {uid} not found in history")
    
    def remove_file(self, file_path):
        """Remove a file from processing history (to allow reprocessing)
        
        :param file_path: Path to the XML file
        """
        abs_path = os.path.abspath(file_path)
        if abs_path in self.history["processed_files"]:
            del self.history["processed_files"][abs_path]
            self._save_history()
            print(f"Removed file {file_path} from history")
        else:
            print(f"File {file_path} not found in history")
    
    def export_report(self, output_file="processing_report.txt"):
        """Export a human-readable processing report
        
        :param output_file: Path to output report file
        """ 
        stats = self.get_statistics() 
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("WOS XML Processing Report\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"Last Updated: {stats['last_updated']}\n\n")
            
            f.write("-"*70 + "\n")
            f.write("Summary Statistics\n")
            f.write("-"*70 + "\n")
            f.write(f"Total Records Processed: {stats['total_records']}\n")
            f.write(f"Total Files Processed: {stats['total_files']}\n")
            f.write(f"Total Errors: {stats['total_errors']}\n\n")
            
            if self.history["processed_files"]:
                f.write("-"*70 + "\n")
                f.write("Processed Files\n")
                f.write("-"*70 + "\n")
                for file_path, info in self.history["processed_files"].items():
                    f.write(f"\nFile: {file_path}\n")
                    f.write(f"  Processed: {info['processed_at']}\n")
                    f.write(f"  Records: {info['record_count']}\n")
                    f.write(f"  Errors: {info['error_count']}\n")
                    f.write(f"  Size: {info['file_size']} bytes\n")
            
            # List errors if any
            errors = [uid for uid, info in self.history["processed_records"].items() 
                     if info.get("error")] 
            
            if errors:
                f.write("\n" + "-"*70 + "\n")
                f.write("Records with Errors\n")
                f.write("-"*70 + "\n")
                for uid in errors[:50]:  # Limit to first 50
                    info = self.history["processed_records"][uid]
                    f.write(f"\nUID: {uid}\n")
                    f.write(f"  Error: {info.get('error_message', 'Unknown')}\n")
                    f.write(f"  Time: {info.get('error_time', 'Unknown')}\n")
                    if info.get('source_file'):
                        f.write(f"  File: {info['source_file']}\n")
                
                if len(errors) > 50:
                    f.write(f"\n... and {len(errors) - 50} more errors\n")
        
        print(f"Report exported to: {output_file}")
    
    def print_summary(self):
        """Print a summary of processing history to console""" 
        stats = self.get_statistics() 
        
        print("\n" + "="*70)
        print("Processing History Summary")
        print("="*70)
        print(f"Total Records Processed: {stats['total_records']}")
        print(f"Total Files Processed: {stats['total_files']}")
        print(f"Total Errors: {stats['total_errors']}")
        print(f"Last Updated: {stats['last_updated']}")
        print("="*70 + "\n")


if __name__ == "__main__":
    """Command-line interface for history management"""
    import sys
    
    manager = ProcessingHistoryManager()
    
    if len(sys.argv) < 2:
        print("\nProcessing History Manager - Command Line Tool")
        print("="*70)
        print("\nUsage:")
        print("  python xml_processing_history.py summary         - Show summary")
        print("  python xml_processing_history.py report          - Export report")
        print("  python xml_processing_history.py reset           - Reset history")
        print("  python xml_processing_history.py check <uid>     - Check record")
        print("  python xml_processing_history.py remove <uid>    - Remove record")
        print()  
        manager.print_summary()
        sys.exit(0)
    
    command = sys.argv[1].lower()
    
    if command == "summary":
        manager.print_summary()
    
    elif command == "report":
        output_file = sys.argv[2] if len(sys.argv) > 2 else "processing_report.txt"
        manager.export_report(output_file)
    
    elif command == "reset":
        manager.reset_history()
    
    elif command == "check":
        if len(sys.argv) < 3:
            print("Error: UID required")
            sys.exit(1)
        uid = sys.argv[2]
        info = manager.get_record_info(uid)
        if info:
            print(f"\nRecord: {uid}")
            print(json.dumps(info, indent=2))
        else:
            print(f"Record {uid} not found in history")
    
    elif command == "remove":
        if len(sys.argv) < 3:
            print("Error: UID required")
            sys.exit(1)
        uid = sys.argv[2]
        manager.remove_record(uid)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)