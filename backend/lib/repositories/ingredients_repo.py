from lib.models.ingredients import Ingredient

class IngredientRepository():
    def __init__(self, connection):
        self._connection = connection
    
    async def get_ingredients_by_recipe_id(self, recipe_id):
        rows = await self._connection.execute(
            'SELECT * FROM ingredients WHERE recipe_id = $1', [recipe_id]
            )
        ingredients = []
        if not rows:
            return None
        else:
            for row in rows:
                ingredient = Ingredient(row["id"], row["recipe_id"], row["ingredient_name"])
                ingredients.append(ingredient)
            return ingredients
        
    async def create_new_ingredient(self, ingredient):
        await self._connection.execute(
            'INSERT INTO ingredients (recipe_id, ingredient_name) VALUES ($1, $2)',
            [ingredient.recipe_id, ingredient.ingredient_name])
        return None 