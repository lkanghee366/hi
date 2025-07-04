#!/usr/bin/env python3
"""
Recipe AI Generator
Generates comprehensive recipe blog posts using Gemini AI and Pixabay images.
"""

import os
import sys
from config.settings import Config
from core.recipe_generator import RecipeGenerator

def main():
    """Main application entry point"""
    print("🍽️ Recipe AI Generator")
    print("=" * 50)
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("Please check your .env file and ensure all required API keys are set.")
        return
    
    # Create output directories
    for path in [Config.OUTPUT_DIR, Config.LOG_DIR]:
        if os.path.exists(path):
            if os.path.isfile(path):
                print(f"❌ Cannot create directory '{path}': a file with the same name exists. Please remove or rename the file.")
                return
            # Directory exists, skip creation
        else:
            os.makedirs(path, exist_ok=True)
    
    # Initialize generator
    generator = RecipeGenerator()
    
    print("Ready to generate recipes! Type 'quit' to exit.\n")
    
    while True:
        try:
            # Get user input
            keyword = input("Enter recipe keyword: ").strip()
            
            if keyword.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not keyword:
                print("❌ Please enter a valid keyword")
                continue
            
            print(f"\n{'='*50}")
            
            # Generate recipe
            result = generator.generate_recipe(keyword)
            
            if result:
                print(f"\n✅ Success! Recipe saved to: {result}")
            else:
                print(f"\n❌ Failed to generate recipe for '{keyword}'")
            
            print(f"{'='*50}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            continue

if __name__ == "__main__":
    main()
