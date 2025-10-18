# API Research & Testing — Day 4 (OpenFoodFacts)

## API chosen
- **OpenFoodFacts** (no API key required) — used for fast testing of food/product nutrition metadata.

## Why chosen
- No signup or API key required → zero friction for Day-4 testing.
- Provides searchable product and nutrition metadata (by name or barcode).

## Test script
- `tests/openfoodfacts_test.py` — sends a search request for "apple" and saves the JSON response to:
  - `docs/api_samples/openfoodfacts_sample.json`

## How to run (local)
1. Activate Python venv:
   - PowerShell: `.venv\Scripts\Activate.ps1`
2. Install dependency:
   - `pip install requests`
3. Run the test:
   - `python tests/openfoodfacts_test.py`

## Files saved
- `docs/api_samples/openfoodfacts_sample.json` — contains the API JSON response (sample).

## Next steps
- Integrate the nutrition lookup into the UI (Health Tips / Nutrition page) using search term input.
- If we need richer nutrition analysis later, consider Nutritionix or Spoonacular (require signup).
