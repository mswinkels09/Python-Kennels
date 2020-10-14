from models.customer import Customer
from models.location import Location
import sqlite3
import json
from models import Animal


ANIMALS = []

def get_all_animals():
    # Open a connection to the database
    with sqlite3.connect("./kennel.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.customer_id,
            a.location_id
        FROM animal a
        """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list(list of tuples)
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        # row = tuple
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            #tuple = comma seperated value
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])
            # __dict__ = turns it into dictionary representation (used to be object in JS)
            animals.append(animal.__dict__)

    # Use `json` package to properly serialize list as JSON
    #.dumps() = converts to json (like jsonstringify)
    return json.dumps(animals)

# Function with a single parameter
def get_single_animal(id):
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name animal_name,
            a.breed,
            a.status,
            a.customer_id,
            a.location_id,
            l.name location_name,
            c.name customer_name
        FROM animal a
        JOIN `Location` l ON l.id = a.location_id
        JOIN `Customer` c ON c.id = a.customer_id
        WHERE a.id = ?
        """, ( id, ))
            #need a comma to make it a tuple (will create errors if no comma)

        # Load the single result into memory(object)
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(data['id'], data['animal_name'], data['breed'], data['status'],
                        data['customer_id'], data['location_id'])

        location = Location("", data['location_name'])
        animal.location = location.__dict__

        customer = Customer("", data['customer_name'])
        animal.customer = customer.__dict__

        return json.dumps(animal.__dict__)

def create_animal(animal):
    # Get the id value of the last animal in the list
    max_id = ANIMALS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    animal["id"] = new_id

    # Add the animal dictionary to the list
    ANIMALS.append(animal)

    # Return the dictionary with `id` property added
    return animal
    
def delete_animal(id):
    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))

        rows_affected = db_cursor.rowcount

        if rows_affected == 0:
            return False
        else:
            return True

def update_animal(id, new_animal):
    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                customer_id = ?
        WHERE id = ?
        """, (new_animal['name'], new_animal['species'],
              new_animal['status'], new_animal['location_id'],
              new_animal['customer_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

def get_animals_by_location(location_id):
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM animal a
        WHERE a.location_id = ?
        """, ( location_id, ))

        animals = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            # Create an animal instance from the current row
            animal = Animal(row['id'], row['name'], row['breed'], row['status'],
                            row['customer_id'], row['location_id'])
            animals.append(animal.__dict__)

        # Return the JSON serialized Customer object
    return json.dumps(animals)

def get_animals_by_status(status):
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM animal a
        WHERE a.status = ?
        """, ( status, ))

        animals = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            # Create an animal instance from the current row
            animal = Animal(row['id'], row['name'], row['breed'], row['status'],
                            row['customer_id'], row['location_id'])
            animals.append(animal.__dict__)

        # Return the JSON serialized Customer object
    return json.dumps(animals)  