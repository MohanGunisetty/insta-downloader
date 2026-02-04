
import instaloader
import asyncio
from typing import Optional, Dict, Any

class DownloaderService:
    def __init__(self):
        self.L = instaloader.Instaloader()
        # Configure to be lightweight
        self.L.save_metadata = False
        self.L.download_video_thumbnails = False
        self.L.post_metadata_txt_pattern = ""
        # We don't want to actually download to disk if we can avoid it, 
        # but if we do, we need a target. We'll handle downloads separately if needed.

    async def get_media_info(self, url: str) -> Dict[str, Any]:
        """
        Extracts media information from an Instagram URL.
        Returns a dictionary with direct download link and metadata.
        """
        shortcode = self._extract_shortcode(url)
        if not shortcode:
            raise ValueError("Invalid Instagram URL: Could not extract shortcode")

        loop = asyncio.get_event_loop()
        # Instaloader is synchronous, run in executor
        try:
            post = await loop.run_in_executor(None, self._get_post, shortcode)
            
            return {
                "shortcode": post.shortcode,
                "media_type": "video" if post.is_video else "image",
                "media_url": post.video_url if post.is_video else post.url,
                "thumbnail_url": post.url if post.is_video else None,  # post.url is usually the cover for videos
                "caption": post.caption,
                "owner": post.owner_username,
                "filename": f"{post.owner_username}_{shortcode}.{'mp4' if post.is_video else 'jpg'}"
            }
        except Exception as e:
            raise ValueError(f"Failed to fetch post metadata: {str(e)}")

    def _get_post(self, shortcode: str) -> instaloader.Post:
        return instaloader.Post.from_shortcode(self.L.context, shortcode)

    def _extract_shortcode(self, url: str) -> Optional[str]:
        """
        Simple extraction of shortcode from URL.
        """
        # Remove query params
        url = url.split('?')[0]
        url = url.rstrip('/')
        
        parts = url.split('/')
        # https://www.instagram.com/p/SHORTCODE/
        # https://www.instagram.com/reel/SHORTCODE/
        if 'p' in parts:
            idx = parts.index('p')
            if len(parts) > idx + 1:
                return parts[idx + 1]
        elif 'reel' in parts:
            idx = parts.index('reel')
            if len(parts) > idx + 1:
                return parts[idx + 1]
        elif 'tv' in parts:
            idx = parts.index('tv')
            if len(parts) > idx + 1:
                return parts[idx + 1]
                
        # Fallback for simple shortcode input or other formats could be added here
        return None
