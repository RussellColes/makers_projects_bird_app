class Ingredient:
    def __init__(self, id, recipe_id, ingredient_name):
        self.id = id
        self.recipe_id = recipe_id
        self.ingredient_name = ingredient_name

    def to_dict(self):
        return {
            "id": self.id,
            "recipe_id": self.recipe_id,
            "ingredient_name": self.ingredient_name,
        }
    
    def __repr__(self):
        return f"Ingredient({self.id}, {self.recipe_id}, {self.ingredient_name})"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__