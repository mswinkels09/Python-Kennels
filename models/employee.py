class Employee():

    # Class initializer. It has 5 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, unique_id, name, address, location_id):
        self.id = unique_id
        self.name = name
        self.address = address
        self.location_id = location_id

