#!/usr/bin/env python3

from app import app
from models import db, Plant

with app.app_context():
    # Clear existing data
    Plant.query.delete()

    # Add new plants to the database with all required fields
    aloe = Plant(
        name="Aloe",  # Make sure 'name' is provided
        image="./images/aloe.jpg",  # Make sure 'image' is provided
        price=11.50  # Make sure 'price' is provided
    )

    zz_plant = Plant(
        name="ZZ Plant",  # Make sure 'name' is provided
        image="./images/zz-plant.jpg",  # Make sure 'image' is provided
        price=25.98  # Make sure 'price' is provided
    )

    # Commit the new plants to the database
    db.session.add_all([aloe, zz_plant])
    db.session.commit()

    print("Plants seeded successfully!")
