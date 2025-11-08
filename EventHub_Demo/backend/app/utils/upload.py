"""
Image upload utility
"""

import os
import uuid
import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from typing import Optional

from app.config import settings


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def validate_image(file: UploadFile) -> None:
    """Validate uploaded image file"""
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )


def generate_unique_filename(original_filename: str) -> str:
    """Generate unique filename"""
    file_ext = Path(original_filename).suffix.lower()
    unique_name = f"{uuid.uuid4().hex}{file_ext}"
    return unique_name


async def save_upload_file(upload_file: UploadFile) -> tuple[str, int]:
    """
    Save uploaded file to disk
    Returns: (filename, file_size)
    """
    # Validate file
    validate_image(upload_file)
    
    # Generate unique filename
    filename = generate_unique_filename(upload_file.filename)
    file_path = Path(settings.UPLOAD_DIR) / filename
    
    # Ensure upload directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save file
    file_size = 0
    try:
        with file_path.open("wb") as buffer:
            while chunk := await upload_file.read(8192):  # Read in chunks
                file_size += len(chunk)
                
                # Check file size
                if file_size > MAX_FILE_SIZE:
                    # Delete partial file
                    file_path.unlink(missing_ok=True)
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"File too large. Max size: {MAX_FILE_SIZE / (1024*1024):.1f}MB"
                    )
                
                buffer.write(chunk)
    except Exception as e:
        # Clean up on error
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )
    
    return filename, file_size


def delete_upload_file(filename: str) -> bool:
    """Delete uploaded file"""
    file_path = Path(settings.UPLOAD_DIR) / filename
    try:
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    except Exception:
        return False


def get_file_url(filename: str, request_base_url: str) -> str:
    """Generate URL for uploaded file"""
    return f"{request_base_url.rstrip('/')}/uploads/{filename}"
