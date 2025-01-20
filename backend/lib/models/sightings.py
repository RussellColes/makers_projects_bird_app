class Sighting:
    def __init__(self, id, bird_name, date_spotted, location, image, user_id):
        self.id = id
        self.bird_name = bird_name
        self.date_spotted = date_spotted
        self.location = location
        self.image = image
        self.user_id = user_id


    def to_dict(self):
        return {
            "id": self.id,
            "bird_name": self.bird_name,
            "date_spotted": self.date_spotted,
            "location": self.location,
            "image": self.image,
            "user_id": self.user_id,
            }

    def __repr__(self):
        return f"User({self.id}, {self.bird_name}, {self.date_spotted}, {self.location}, {self.image}, {self.user_id})"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__