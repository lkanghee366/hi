import requests
import time
from typing import List, Optional
from config.settings import Config

class PixabayService:
    def __init__(self):
        self.api_key = Config.PIXABAY_API_KEY
        self.base_url = "https://pixabay.com/api/"
    
    def search_food_images(self, keyword: str) -> List[str]:
        """Search for food images and return 3 URLs"""
        params = {
            'key': self.api_key,
            'q': keyword,
            'image_type': 'photo',
            'orientation': Config.IMAGE_ORIENTATION,
            'category': 'food',
            'safesearch': 'true',
            'per_page': 10,  # Get 10 to have options
            'order': 'popular'
        }
        
        try:
            response = requests.get(
                self.base_url, 
                params=params, 
                timeout=Config.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            images = data.get('hits', [])
            
            if not images:
                print(f"⚠️ No images found for '{keyword}' on Pixabay")
                return self._get_placeholder_images()
            
            # Extract first 3 image URLs
            image_urls = []
            for img in images[:Config.IMAGES_PER_RECIPE]:
                url = img.get(Config.IMAGE_SIZE) or img.get('webformatURL')
                if url:
                    image_urls.append(url)
            
            # Ensure we have exactly 3 images
            while len(image_urls) < Config.IMAGES_PER_RECIPE:
                image_urls.append(self._get_placeholder_images()[0])
            
            print(f"✅ Retrieved {len(image_urls)} images for '{keyword}'")
            return image_urls[:Config.IMAGES_PER_RECIPE]
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Pixabay API error: {e}")
            return self._get_placeholder_images()
        except Exception as e:
            print(f"❌ Unexpected error in image search: {e}")
            return self._get_placeholder_images()
    
    def _get_placeholder_images(self) -> List[str]:
        """Return placeholder image URLs when search fails"""
        return [
            "https://via.placeholder.com/640x480/FFE4B5/8B4513?text=Recipe+Image",
            "https://via.placeholder.com/640x480/F0E68C/8B4513?text=Ingredients",
            "https://via.placeholder.com/640x480/DDA0DD/8B4513?text=Cooking+Process"
        ]
