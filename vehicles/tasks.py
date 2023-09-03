from celery import shared_task
from datetime import datetime
from .models import Vehicle, VehicleMake


@shared_task
def create_vehicle(item):
    try:
        make_name = item["Make"]
        year = item["Year"]
        model = item["Model"]
        category = item["Category"]

        # Check if the Make already exists or create a new one
        make, _ = VehicleMake.objects.get_or_create(name=make_name)

        # Create a new Vehicle object
        vehicle = Vehicle(
            year=year,
            make=make,
            model=model,
            category=category,
        )

        # Save the Vehicle object to the database
        vehicle.save()
        print(vehicle)
    except Exception as e:
        print("error", e)
