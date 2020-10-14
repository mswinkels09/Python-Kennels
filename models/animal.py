class Animal():

    # Class initializer. It has 5 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    #turns wthe table info into data python can use
    def __init__(self, unique_id, name, breed, status, customer_id, location_id):
        self.id = unique_id
        self.name = name
        self.breed = breed
        self.status = status
        self.customer_id = customer_id
        self.location_id = location_id
        self.location = None
        self.customer = None

