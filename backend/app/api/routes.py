
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.models.schemas import DownloadRequest, DownloadResponse, MediaInfo
from app.services.url_processor import UrlProcessor
from app.services.downloader import DownloaderService
import uuid

router = APIRouter()
url_processor = UrlProcessor()
downloader_service = DownloaderService()

# In-memory job store for demo purposes 
# (in production, use Redis)
jobs = {}

@router.post("/download", response_model=DownloadResponse)
async def download_media(request: DownloadRequest):
    """
    Accepts a list of URLs. 
    If 1 URL, tries to return direct link immediately.
    If multiple, creates a background job.
    """
    valid_urls = url_processor.process_batch(request.urls)
    
    if not valid_urls:
        raise HTTPException(status_code=400, detail="No valid Instagram URLs provided")
        
    # Single URL direct response
    if len(valid_urls) == 1:
        try:
            url = valid_urls[0]
            info = await downloader_service.get_media_info(url)
            return DownloadResponse(
                message="Success",
                results=[info]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
            
    # Bulk - create job (placeholder logic for now)
    job_id = str(uuid.uuid4())
    # TODO: Implement actual background job processing for bulk
    # For now, we'll just return the first one as a demo fallback or implement simple loop
    # Ideally, we push to a queue. Here we'll just fail for bulk in v0.1 to keep it simple 
    # and focused on the core "Single Download" functionality first as per Phase 1 priority.
    
    # Actually, let's just attempt to do them all currently for the demo if < 5
    if len(valid_urls) <= 5:
        results = []
        errors = []
        for url in valid_urls:
            try:
                info = await downloader_service.get_media_info(url)
                results.append(info)
            except Exception as e:
                errors.append(f"Failed {url}: {str(e)}")
        
        return DownloadResponse(
            message=f"Processed {len(results)}/{len(valid_urls)} URLs",
            results=results
        )

    return DownloadResponse(message="Bulk download > 5 not yet supported in v0.1", results=[])

@router.get("/health")
async def health_check():
    return {"status": "ok"}
