"""
Upload Router
Handle file uploads (images)
"""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.auth import get_current_user, Auth0User
from app.utils.upload import save_upload_file, get_file_url
from app.schemas import ImageUploadResponse


router = APIRouter()


@router.post("/image", response_model=ImageUploadResponse)
async def upload_image(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Auth0User = Depends(get_current_user)
):
    """Upload an image file"""
    try:
        filename, file_size = await save_upload_file(file)
        
        # Generate URL
        base_url = str(request.base_url)
        file_url = get_file_url(filename, base_url)
        
        return ImageUploadResponse(
            filename=filename,
            url=file_url,
            size=file_size
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image: {str(e)}"
        )
