class Step:
    def __init__(self, id, recipe_id, step_order, step_description):
        self.id = id
        self.recipe_id = recipe_id
        self.step_order = step_order
        self.step_description = step_description

    def to_dict(self):
        return {
            "id": self.id,
            "recipe_id": self.recipe_id,
            "step_order": self.step_order,
            "step_description": self.step_description,
            }
    
    def __repr__(self):
        return f"Step({self.id}, {self.recipe_id}, {self.step_order}, {self.step_description})"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__