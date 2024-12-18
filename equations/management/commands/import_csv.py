import csv
from django.core.management import base
from equations.models import Mathematician

class Command(base.BaseCommand):
    help = "importing mathematicians from csv"
    with open("data_cleaned.csv", mode="r", encoding = "utf-8") as file:
        reader = csv.DictReader(file) #file reader

        for row in reader:
            field = row["field of work"] if row["field of work"] else row["occupation"]

            Mathematician.objects.create(
                name = row["mathematicians"],
                fields = field
            )
