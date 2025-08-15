import os
import shutil
import time
from pathlib import Path
from typing import Optional, Tuple
from fastapi import UploadFile
from app.utils.logging import get_logger

logger = get_logger(__name__)

class FileUtils:
    def __init__(self, uploads_dir: str = "uploads"):
        self.uploads_dir = Path(uploads_dir)
        self.uploads_dir.mkdir(exist_ok=True)
    
    async def save_uploaded_file(self, file: UploadFile) -> Tuple[bool, str, str]:
        """Save uploaded file and return success status, filename, and filepath"""
        try:
            # Generate unique filename
            timestamp = int(time.time())
            file_extension = Path(file.filename).suffix if file.filename else ""
            filename = f"upload_{timestamp}{file_extension}"
            filepath = self.uploads_dir / filename
            
            # Save file
            with open(filepath, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            logger.info(f"File saved successfully: {filename}")
            return True, filename, str(filepath)
            
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            return False, "", ""
    
    def get_file_info(self, filepath: str) -> dict:
        """Get file information"""
        try:
            path = Path(filepath)
            if not path.exists():
                return {}
            
            stat = path.stat()
            return {
                "filename": path.name,
                "size_bytes": stat.st_size,
                "created_time": stat.st_ctime,
                "modified_time": stat.st_mtime,
                "is_file": path.is_file(),
                "is_directory": path.is_directory()
            }
        except Exception as e:
            logger.error(f"Error getting file info: {str(e)}")
            return {}
    
    def cleanup_old_files(self, max_age_hours: int = 24) -> int:
        """Clean up old files from uploads directory"""
        try:
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            cleaned_count = 0
            
            for file_path in self.uploads_dir.iterdir():
                if file_path.is_file():
                    file_age = current_time - file_path.stat().st_mtime
                    if file_age > max_age_seconds:
                        file_path.unlink()
                        cleaned_count += 1
                        logger.info(f"Cleaned up old file: {file_path.name}")
            
            logger.info(f"Cleanup completed: {cleaned_count} files removed")
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
            return 0
    
    def get_uploads_directory_size(self) -> int:
        """Get total size of uploads directory in bytes"""
        try:
            total_size = 0
            for file_path in self.uploads_dir.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
            return total_size
        except Exception as e:
            logger.error(f"Error calculating directory size: {str(e)}")
            return 0
