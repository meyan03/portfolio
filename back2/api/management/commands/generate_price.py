# api/management/commands/generate_price.py
from django.core.management.base import BaseCommand
from api.models import Product
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Generate random prices for all products'

    def handle(self, *args, **options):
        self.stdout.write("Starting price generation...")

        products = Product.objects.all()
        count = 0

        for product in products:
            price = round(random.uniform(1.0, 10.0), 2)
            product.price = Decimal(str(price))
            product.save()
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully updated prices for {count} products"))
