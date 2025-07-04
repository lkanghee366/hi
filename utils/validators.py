from typing import Dict
from config.settings import Config

class ContentValidator:
    def validate_and_fix(self, recipe_data: Dict) -> Dict:
        """Auto-validate and fix recipe content with more robust checks."""
        
        # Các giá trị và cấu trúc mặc định
        defaults = {
            'title': "Recipe Title",
            'rating': 4.5,
            'review_count': 100,
            'difficulty': 'Medium',
            'prep_time': 15,
            'cook_time': 30,
            'servings': 4,
            'introduction': {"paragraph1": "", "paragraph2": ""},
            'ingredients': [],
            'instructions': [],
            'nutrition': {},
            'variations': [],
            'storage': [],
            'faqs': [],
            'tips': []
        }
        
        # Đảm bảo các key chính tồn tại
        for key, default_value in defaults.items():
            if key not in recipe_data or not recipe_data[key]:
                recipe_data[key] = default_value
        
        # Kiểm tra kiểu dữ liệu cho các trường thời gian
        for time_key in ['prep_time', 'cook_time']:
            if not isinstance(recipe_data.get(time_key), int):
                recipe_data[time_key] = defaults[time_key]
        
        # Tính toán total_time nếu không có hoặc sai
        recipe_data['total_time'] = recipe_data['prep_time'] + recipe_data['cook_time']
        
        # Đảm bảo số lượng tối thiểu cho ingredients và instructions
        if len(recipe_data['ingredients']) < Config.MIN_INGREDIENTS:
            recipe_data['ingredients'].extend(
                [f"Missing ingredient {i+1}" for i in range(Config.MIN_INGREDIENTS - len(recipe_data['ingredients']))]
            )
        
        if len(recipe_data['instructions']) < Config.MIN_STEPS:
            recipe_data['instructions'].extend(
                [f"Missing step {i+1}" for i in range(Config.MIN_STEPS - len(recipe_data['instructions']))]
            )
        
        return recipe_data
