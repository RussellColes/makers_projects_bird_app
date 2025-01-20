class Recipe:
    def __init__(self, id, title, date_created, cooking_time, bird_sighting_id, avg_rating=None):
        self.id = id
        self.title = title
        self.date_created = date_created
        self.cooking_time = cooking_time
        self.bird_sighting_id = bird_sighting_id
        self.avg_rating = avg_rating

        print("self.title from line 10 --> ", self.title)
        print("self.datecreated from line 11 --> ", self.date_created)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "date_created": self.date_created,
            "cooking_time": self.cooking_time,
            "bird_sighting_id": self.bird_sighting_id,
            "avg_rating": self.avg_rating
        }

    def __repr__(self):
        return f"Recipe({self.id}, {self.title}, {self.date_created}, {self.cooking_time}, {self.bird_sighting_id}, {self.avg_rating})"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__









