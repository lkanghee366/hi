import os
import re
from datetime import datetime
from config.settings import Config

class FileManager:
    def save_recipe(self, html_content: str, keyword: str) -> str:
        """Save recipe HTML to file"""
        # Create safe filename
        safe_keyword = re.sub(r'[^a-zA-Z0-9\s]', '', keyword)
        safe_keyword = re.sub(r'\s+', '_', safe_keyword.strip())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_keyword.lower()}_{timestamp}.html"
        
        # Full file path
        filepath = os.path.join(Config.OUTPUT_DIR, filename)
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
