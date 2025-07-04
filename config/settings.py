import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-pro-latest')
    
    # Recipe Configuration
    MIN_INGREDIENTS = 6
    MAX_INGREDIENTS = 12
    MIN_STEPS = 4
    MAX_STEPS = 8
    FAQ_COUNT = 7
    TIPS_COUNT = 7
    VARIATION_COUNT = 4
    STORAGE_SECTIONS = 4
    
    # SEO Configuration
    KEYWORD_APPEARANCE_TARGET = 6  # 6-7 times
    
    # Image Configuration
    IMAGES_PER_RECIPE = 3
    IMAGE_ORIENTATION = 'horizontal'
    IMAGE_SIZE = 'webformatURL'  # Pixabay size option
    
    # Output Configuration
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'output/recipes')
    LOG_DIR = os.getenv('LOG_DIR', 'output/logs')
    
    # API Limits
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required_keys = ['GEMINI_API_KEY', 'PIXABAY_API_KEY']
        missing = [key for key in required_keys if not getattr(cls, key)]
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")