import json
import os

# Define the path to your saved sample API response file
# Adjust 'JSON_PATH' if  'docs' folder is structured differently
JSON_PATH = 'docs/api_samples/openfoodfacts_sample.json' 

def get_nutrition_data():
    """
    Reads the OpenFoodFacts sample JSON and extracts key nutrition metrics
    for the first product found to display in the Streamlit UI.
    """
    # Check if the file exists (crucial for a robust application)
    if not os.path.exists(JSON_PATH):
        print(f"Error: Nutrition sample file not found at {JSON_PATH}")
        return None

    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # We extract data from the first product entry for the demo
        if 'products' in data and data['products']:
            product = data['products'][0] 
            nutriments = product.get('nutriments', {})

            # Extract specific metrics (per 100g)
            return {
                "name": product.get('product_name', 'Unnamed Product'),
                "calories_100g": nutriments.get('energy-kcal_100g', 0), # Calories
                "proteins_100g": nutriments.get('proteins_100g', 0),
                "sugars_100g": nutriments.get('sugars_100g', 0),
                "fat_100g": nutriments.get('fat_100g', 0)
            }
        else:
            return None # No products found
            
    except Exception as e:
        print(f"Error reading or parsing JSON file: {e}")
        return None