import os
import json
from datetime import datetime
from typing import Dict, Optional
from jinja2 import Template

from services.gemini_service import GeminiService
from services.pixabay_service import PixabayService
from utils.validators import ContentValidator
from utils.file_manager import FileManager
from config.settings import Config

class RecipeGenerator:
    def __init__(self):
        self.gemini = GeminiService()
        self.pixabay = PixabayService()
        self.validator = ContentValidator()
        self.file_manager = FileManager()
    
    def generate_recipe(self, keyword: str) -> Optional[str]:
        """Main method to generate complete recipe"""
        print(f"🍳 Starting recipe generation for: '{keyword}'")
        
        # Phase 1: Extract image search keyword
        print("🔍 Phase 1: Extracting image keyword...")
        image_keyword = self.gemini.extract_image_keyword(keyword)
        print(f"   └── Image keyword: '{image_keyword}'")
        
        # Phase 2: Search for images
        print("📸 Phase 2: Searching for images...")
        image_urls = self.pixabay.search_food_images(image_keyword)
        print(f"   └── Found {len(image_urls)} images")
        
        # Phase 3: Generate base recipe content
        print("🤖 Phase 3: Generating recipe content...")
        recipe_data = self.gemini.generate_recipe_content(keyword)
        if not recipe_data:
            print("❌ Failed to generate recipe content")
            return None
        
        # Phase 4: Auto-validate content
        print("✅ Phase 4: Validating content...")
        recipe_data = self.validator.validate_and_fix(recipe_data)
        
        # Phase 5: Enhance for SEO
        print("✨ Phase 5: Enhancing content for SEO...")
        enhanced_data = self.gemini.enhance_content_for_seo(recipe_data, keyword)
        if enhanced_data:
            recipe_data = enhanced_data
            print("   └── Content enhanced successfully")
        else:
            print("   └── Using base content (enhancement failed)")
        
        # Phase 6: Generate alt texts
        print("🏷️ Phase 6: Generating alt texts...")
        alt_texts = self.gemini.generate_alt_texts(keyword, image_urls)
        
        # Phase 7: Prepare final data
        print("🔄 Phase 7: Consolidating data...")
        final_data = {
            'recipe': recipe_data,
            'images': {
                'hero': {'url': image_urls[0], 'alt': alt_texts[0]},
                'ingredients': {'url': image_urls[1], 'alt': alt_texts[1]},
                'process': {'url': image_urls[2], 'alt': alt_texts[2]}
            },
            'keyword': keyword,
            'stars': self._generate_stars(recipe_data.get('rating', 5.0))
        }
        
        # Phase 8: Generate HTML
        print("📝 Phase 8: Generating HTML...")
        html_content = self._render_template(final_data)
        if not html_content:
            print("❌ Failed to generate HTML")
            return None
        
        # Phase 9: Save file
        print("💾 Phase 9: Saving file...")
        filename = self.file_manager.save_recipe(html_content, keyword)
        
        # Phase 10: Log generation stats
        self._log_generation_stats(keyword, recipe_data, image_urls, filename)
        
        print(f"🎉 Recipe generated successfully: {filename}")
        return filename
    
    def _generate_stars(self, rating: float) -> str:
        """Generate star display from rating"""
        full_stars = int(rating)
        half_star = 1 if rating % 1 >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star
        
        return '★' * full_stars + '☆' * half_star + '☆' * empty_stars
    
    def _render_template(self, data: Dict) -> Optional[str]:
        """Render HTML template with data"""
        try:
            template_path = os.path.join('templates', 'recipe_body.html')
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            template = Template(template_content)
            return template.render(**data)
            
        except Exception as e:
            print(f"❌ Template rendering error: {e}")
            return None
    
    def _log_generation_stats(self, keyword: str, recipe_data: Dict, image_urls: List, filename: str):
        """Log generation statistics"""
        stats = {
            'timestamp': datetime.now().isoformat(),
            'keyword': keyword,
            'filename': filename,
            'ingredients_count': len(recipe_data.get('ingredients', [])),
            'steps_count': len(recipe_data.get('instructions', [])),
            'faqs_count': len(recipe_data.get('faqs', [])),
            'tips_count': len(recipe_data.get('tips', [])),
            'images_retrieved': len(image_urls),
            'rating': recipe_data.get('rating'),
            'difficulty': recipe_data.get('difficulty')
        }
        
        print(f"📊 Generation Stats:")
        print(f"   ├── Ingredients: {stats['ingredients_count']}")
        print(f"   ├── Steps: {stats['steps_count']}")
        print(f"   ├── FAQs: {stats['faqs_count']}")
        print(f"   ├── Tips: {stats['tips_count']}")
        print(f"   ├── Images: {stats['images_retrieved']}")
        print(f"   └── Rating: {stats['rating']}/5.0")
