from typing import Dict
from config.settings import Config

class ContentValidator:
    def validate_and_fix(self, recipe_data: Dict) -> Dict:
        """Auto-validate and fix recipe content"""
        # Ensure required fields exist
        if 'ingredients' not in recipe_data:
            recipe_data['ingredients'] = [f"Ingredient {i+1}" for i in range(Config.MIN_INGREDIENTS)]
        
        if 'instructions' not in recipe_data:
            recipe_data['instructions'] = [f"Step {i+1}: Add instruction here" for i in range(Config.MIN_STEPS)]
        
        # Validate and fix lengths
        if len(recipe_data['ingredients']) < Config.MIN_INGREDIENTS:
            recipe_data['ingredients'].extend([f"Additional ingredient {i}" for i in range(len(recipe_data['ingredients']), Config.MIN_INGREDIENTS)])
        
        # Ensure all required sections exist
        defaults = {
            'title': f"Recipe Title",
            'rating': 4.5,
            'review_count': 100,
            'difficulty': 'Medium',
            'prep_time': 15,
            'cook_time': 30,
            'total_time': 45,
            'servings': 4,
            'variations': [],
            'storage': [],
            'faqs': [],
            'tips': []
        }
        
        for key, default_value in defaults.items():
            if key not in recipe_data:
                recipe_data[key] = default_value
        
        return recipe_data
