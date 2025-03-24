# Import 50 products from Open Food Facts API and save them to the SQLite database
import requests
import json
from django.core.management.base import BaseCommand
from api.models import Product

class Command(BaseCommand):
    help = 'Fetch 50 products from Open Food Facts API and save them to the SQLite database'

    def handle(self, *args, **kwargs):
        # API endpoint to fetch products
        url = "https://world.openfoodfacts.org/cgi/search.pl"
        params = {
            "action": "process",
            "json": 1,
            "page_size": 50,  # Fetch 50 items
            "page": 1,
            "tagtype_0": "categories",  # Filter by category
            "tag_contains_0": "contains",
            "tag_0": "snacks",  # Specific category (e.g., snacks)
        }

        # Make the API request
        response = requests.get(url, params=params)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('Failed to fetch data from Open Food Facts API'))
            return

        # Parse the JSON response
        data = response.json()
        products = data.get('products', [])

        # Save each product to the database
        for product_data in products:
            barcode = product_data.get('code', '')  # Fetch barcode

            # Ensure barcode is not empty before saving
            if not barcode:
                self.stdout.write(self.style.WARNING(f'Skipping product without barcode: {product_data.get("product_name", "Unknown Product")}'))
                continue

            # Map API data to the Product model
            product, created = Product.objects.update_or_create(
                barcode=barcode,  # Use barcode as a unique identifier
                defaults={
                    "name": product_data.get('product_name', ''),
                    "price": self._parse_price(product_data.get('product_price', '')),
                    "brand": product_data.get('brands', ''),
                    "picture": product_data.get('image_url', ''),
                    "category": product_data.get('categories', ''),
                    "nutritional_info": json.dumps(product_data.get('nutriments', {})),
                    "available_quantity": 0,  # Default value, as this is not provided by the API
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully saved product: {product.name}'))
            else:
                self.stdout.write(self.style.NOTICE(f'Updated existing product: {product.name}'))

    def _parse_price(self, price_str):
        """Helper function to parse price from a string to a Decimal."""
        try:
            return float(price_str) if price_str else None
        except (ValueError, TypeError):
            return None
