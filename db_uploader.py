import os, django, csv, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "watcu.settings")
django.setup()

from products.models import Product

CSV_PATH_PRODUCTS = 'products.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)

    for row in data_reader:
        korean_name = row[1]
        english_name = row[2]
        price = row[3]
        description = row[4]
        category_id = row[5]

        Product.objects.create(
            korean_name = korean_name,
            english_name = english_name,
            price = price,
            description = description,
            category_id = category_id,
        )
        