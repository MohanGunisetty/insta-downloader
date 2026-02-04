
from typing import List
import re

class UrlProcessor:
    def __init__(self):
        # Basic validation pattern
        self.instagram_pattern = re.compile(r'https?://(www\.)?instagram\.com/(p|reel|tv)/([^/?#&]+).*')

    def normalize(self, url: str) -> str:
        """
        Cleans and normalizes the URL.
        """
        url = url.strip()
        # Enforce https
        if url.startswith('http://'):
            url = 'https://' + url[7:]
        elif not url.startswith('https://'):
            url = 'https://' + url
            
        # Ensure it's www.instagram.com (optional, but consistent)
        if 'instagram.com' in url and 'www.instagram.com' not in url:
            url = url.replace('instagram.com', 'www.instagram.com')
            
        return url

    def validate(self, url: str) -> bool:
        """
        Checks if the URL is a potentially valid Instagram media link.
        """
        return bool(self.instagram_pattern.match(url))

    def process_batch(self, urls: List[str]) -> List[str]:
        """
        Validates, normalizes, and deduplicates a batch of URLs.
        """
        valid_urls = []
        seen = set()
        
        for url in urls:
            normalized = self.normalize(url)
            if normalized in seen:
                continue
            
            if self.validate(normalized):
                valid_urls.append(normalized)
                seen.add(normalized)
                
        return valid_urls
