class Rating:
    def __init__(self, id, rating_score, recipe_id):
        self.id = id
        self.rating_score = rating_score
        self.recipe_id = recipe_id

    def to_dict(self):
        return {
            "id": self.id,
            "rating_score": self.rating_score,
            "recipe_id": self.recipe_id
        }

    def __repr__(self):
        return f"Rating({self.id}, {self.rating_score}, {self.recipe_id})"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
