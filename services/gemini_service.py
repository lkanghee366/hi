import google.generativeai as genai
import json
import time
import re  # Thêm import re
from typing import Dict, Optional
from config.settings import Config

class GeminiService:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
    
    def extract_image_keyword(self, recipe_keyword: str) -> Optional[str]:
        """Extract optimal image search keyword from recipe keyword"""
        prompt = f"""
        Extract the best single search term from '{recipe_keyword}' for food photography search on Pixabay.
        
        Rules:
        - Return only 1-2 words maximum
        - Focus on the main food item or cooking method
        - Avoid overly specific terms
        - Ensure good image results
        
        Examples:
        - "grilled chicken breast" → "grilled chicken"
        - "chocolate chip cookies" → "chocolate cookies"
        - "beef stir fry" → "stir fry"
        
        Respond with only the search term, no quotes or explanation.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip().replace('"', '').replace("'", "")
        except Exception as e:
            print(f"⚠️ Image keyword extraction failed: {e}")
            # Sửa lỗi: Nối 2 từ đầu tiên thành một
            return ' '.join(recipe_keyword.split()[:2])
    
    def generate_recipe_content(self, keyword: str) -> Optional[Dict]:
        """Generate complete recipe content structure"""
        prompt = f"""
        You are a professional recipe developer. Create a comprehensive recipe for "{keyword}".
        
        Requirements:
        - Compelling title including the keyword
        - Realistic difficulty, timing, servings
        - {Config.MIN_INGREDIENTS}-{Config.MAX_INGREDIENTS} ingredients
        - {Config.MIN_STEPS}-{Config.MAX_STEPS} detailed cooking steps
        - 2-paragraph introduction
        - Accurate nutrition information
        - {Config.VARIATION_COUNT} recipe variations
        - {Config.STORAGE_SECTIONS} storage sections
        - {Config.FAQ_COUNT} practical FAQs
        - {Config.TIPS_COUNT} professional tips
        
        Respond in valid JSON format:
        {{
            "title": "Recipe title with keyword",
            "rating": 4.7,
            "review_count": 156,
            "difficulty": "Easy|Medium|Hard",
            "prep_time": 15,
            "cook_time": 25,
            "total_time": 40,
            "servings": 4,
            "introduction": {{
                "paragraph1": "First intro paragraph (100-120 words)...",
                "paragraph2": "Second intro paragraph (80-100 words)..."
            }},
            "ingredients": [
                "ingredient 1 with measurements",
                "ingredient 2 with measurements"
            ],
            "instructions": [
                "Step 1: Detailed instruction...",
                "Step 2: Detailed instruction..."
            ],
            "nutrition": {{
                "calories": 165,
                "total_fat": "8g (10% DV)",
                "saturated_fat": "1.5g (8% DV)",
                "cholesterol": "65mg (22% DV)",
                "sodium": "590mg (26% DV)",
                "total_carbs": "1g (0% DV)",
                "fiber": "0g (0% DV)",
                "sugars": "0g",
                "protein": "25g (50% DV)"
            }},
            "variations": [
                {{
                    "title": "Variation Name",
                    "description": "Detailed description (50-70 words)..."
                }}
            ],
            "storage": [
                {{
                    "title": "Storage Section Title",
                    "content": "Detailed storage info (60-80 words)..."
                }}
            ],
            "faqs": [
                {{
                    "question": "Practical cooking question?",
                    "answer": "Helpful detailed answer (40-60 words)..."
                }}
            ],
            "tips": [
                {{
                    "title": "Pro Tip Title",
                    "content": "Actionable tip content (40-60 words)..."
                }}
            ]
        }}
        """
        
        return self._make_request_with_retry(prompt)
    
    def enhance_content_for_seo(self, recipe_data: Dict, keyword: str) -> Optional[Dict]:
        """Enhance content for SEO optimization"""
        prompt = f"""
        Enhance the recipe content for SEO optimization with keyword "{keyword}".
        
        Current recipe: {json.dumps(recipe_data)}
        
        SEO Requirements:
        - Naturally integrate "{keyword}" exactly {Config.KEYWORD_APPEARANCE_TARGET}-{Config.KEYWORD_APPEARANCE_TARGET + 1} times throughout content
        - Expand variations to 2-3 sentences each with specific ingredients and serving suggestions
        - Make storage instructions more comprehensive (3-4 sentences each)
        - Ensure FAQs address common cooking concerns
        - Make tips practical and actionable
        - Maintain natural language flow
        - Keep JSON structure identical
        
        Return the enhanced recipe in the same JSON format.
        """
        
        return self._make_request_with_retry(prompt)
    
    def generate_alt_texts(self, keyword: str, image_urls: list) -> list:
        """Generate SEO-friendly alt texts for images"""
        prompt = f"""
        Generate 3 SEO-friendly alt text descriptions for "{keyword}" recipe images.
        
        Images are positioned:
        1. Hero image (after recipe info)
        2. Ingredients image (after ingredients section)  
        3. Process/final dish image (after cooking steps)
        
        Requirements:
        - Include "{keyword}" naturally in each alt text
        - 8-12 words per alt text
        - Descriptive but concise
        - SEO-optimized
        
        Respond with only 3 lines, one alt text per line.
        """
        
        try:
            response = self.model.generate_content(prompt)
            alt_texts = [line.strip() for line in response.text.strip().split('\n') if line.strip()]
            return alt_texts[:3]  # Ensure exactly 3 alt texts
        except Exception as e:
            print(f"⚠️ Alt text generation failed: {e}")
            return [
                f"Delicious {keyword} ready to serve",
                f"Fresh ingredients for {keyword} recipe",
                f"Step by step {keyword} cooking process"
            ]

    def _make_request_with_retry(self, prompt: str) -> Optional[Dict]:
        """Make Gemini API request with robust parsing and retry logic."""
        for attempt in range(Config.MAX_RETRIES):
            try:
                print(f"   └── Making Gemini API request (Attempt {attempt + 1}/{Config.MAX_RETRIES})...")
                response = self.model.generate_content(prompt)
                
                # ---- BẮT ĐẦU PHẦN CẢI TIẾN ----
                
                raw_text = response.text.strip()

                # Làm sạch nội dung nếu nó được bọc trong markdown code block
                if raw_text.startswith('```json'):
                    raw_text = re.sub(r'^```json\s*', '', raw_text)
                    raw_text = re.sub(r'```$', '', raw_text)
                    raw_text = raw_text.strip()

                # Kiểm tra nếu nội dung bị rỗng sau khi làm sạch
                if not raw_text:
                    print(f"⚠️ Warning: Gemini API returned an empty response (Attempt {attempt + 1}).")
                    raise ValueError("Empty response received from API")

                # Parse JSON
                return json.loads(raw_text)
                
                # ---- KẾT THÚC PHẦN CẢI TIẾN ----

            except json.JSONDecodeError as e:
                print(f"⚠️ JSON parsing error (Attempt {attempt + 1}): {e}")
                print("   └── Gemini did not return a valid JSON. Retrying...")
                # Không cần trả về None ngay, vòng lặp sẽ tiếp tục
            
            except Exception as e:
                # Bắt các lỗi khác như ValueError từ chuỗi rỗng
                print(f"⚠️ Gemini API error (Attempt {attempt + 1}): {e}")

            # Nếu không phải lần thử cuối, chờ trước khi thử lại
            if attempt < Config.MAX_RETRIES - 1:
                sleep_time = 2 ** (attempt + 1)
                print(f"   └── Waiting for {sleep_time} seconds before retrying...")
                time.sleep(sleep_time)
        
        print("❌ All retry attempts failed. Could not get valid data from Gemini.")
        return None
