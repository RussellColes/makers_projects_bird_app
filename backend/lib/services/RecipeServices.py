from lib.recipe_templates.recipe_templetes import *
from lib.models.ingredients import Ingredient
from lib.models.steps import Step
from lib.models.sightings import Sighting
from lib.models.recipes import Recipe
import random

class RecipeService:
    def __init__(self, sightings_repo, recipes_repo, ingredients_repo, steps_repo, connection):
        self.sightings_repo = sightings_repo
        self.recipes_repo = recipes_repo
        self.ingredients_repo = ingredients_repo
        self.steps_repo = steps_repo
        self._connection = connection

    def select_random_recipe(self):
        recipe_choices = [
            HERB_GLAZED_RECIPE,
            POT_PIE_RECIPE,
            FRIED_RICE_RECIPE,
            A_LORANGE_RECIPE,
            PASTA_BAKE_RECIPE,
            JAMAICAN_JERK_RECIPE,
            BUFFALO_WINGS_RECIPE,
            HOMESTYLE_CURRY_RECIPE,
            CLASSIC_PARM_RECIPE,
            PEANUT_LIME_NOODLE_RECIPE,
            LASAGNE_RECIPE,
            CREAMY_TUSCAN_RECIPE,
            SHAWARMA_SPICED_WRAPS_RECIPE
        ]
        selected = random.choice(recipe_choices)
        return selected 

    # helper function to populate the template with given birdname --> move to utils folder later
    def _populate_bird_template(self, template, bird_name):

        populated = {
            "title": template["title"].replace("{BIRD}", bird_name),
            "cooking_time": template["cooking_time"],
            "ingredients": [],
            "steps": []
        }

        for ing in template["ingredients"]:
            populated["ingredients"].append({
                "ingredient_name": ing["ingredient_name"].replace("{BIRD}", bird_name)
            })

        for st in template["steps"]:
            populated["steps"].append({
                "step_order": st["step_order"],
                "step_description": st["step_description"].replace("{BIRD}", bird_name)
            })

        return populated
    
    async def create_recipe_from_bird_name(self, bird_name, user_id, location, image):
        try:
            # 1. Create a bird sighting
            new_sighting = Sighting(
                None, #id --> generated by database upon creation
                bird_name,
                None, # date_spotted --> auto set in repo
                location, # location --> defaults to "Unknown" in database
                image, 
                user_id
            )
            # 2. Add sighting to database
            sighting_id = await self.sightings_repo.create_bird_sighting(new_sighting)
            if not sighting_id:
                raise Exception("Failed to create bird sighting.")
            


            # BUG in steps  below, which intermittently causes the 'ingredient_name' to fail.
            # Needs investigating
            
            
            
            
            
            # 3. select random recipe
            random_recipe = self.select_random_recipe()
            print("random recipe title line 83 -->", random_recipe["title"])

            # 4. Populate the template with the given bird name
            recipe_data = self._populate_bird_template(random_recipe, bird_name)
            print("recipe data title line 87 -->", recipe_data)

            # 5. Create the recipe in bird_recipes
            new_recipe = Recipe(
                None, #id
                recipe_data["title"], #recipe title
                None, # date_created --> auto set in repo
                recipe_data["cooking_time"], #cooking_time
                sighting_id, # bird_sighting_id
                None #average rating
            )
            recipe_id = await self.recipes_repo.create_recipe(new_recipe)
            print("this shows the newly created recipe id - line 98", recipe_id)
            if not recipe_id:
                raise Exception("Failed to create recipe.")
            
            # 5. Insert ingredients
            print("""recipe_data["ingredients"] --> """, recipe_data["ingredients"])
            for ing in recipe_data["ingredients"]:
                ingredient = Ingredient(
                    None, #id
                    recipe_id,
                    ing["ingredient_name"] # ingredient_name
                )
                await self.ingredients_repo.create_new_ingredient(ingredient)

            # 6. Insert steps
            for stp in recipe_data["steps"]:
                step = Step(
                    None,
                    recipe_id,
                    stp["step_order"],
                    stp["step_description"]
                )
                await self.steps_repo.create_new_step(step)

            # Return the recipe_id 
            return recipe_id
        
        # handle creation errors
        except Exception as e:
            print(f"Error creating recipe: {e}")
            return None
        
    async def get_recipe_from_sighting_id(self, sighting_id):
        recipe = await self.recipes_repo.get_single_recipe(sighting_id)
        print(recipe)
        if not recipe:
            raise Exception("Failed to fetch recipe.")
        print(recipe.id)
        ingredients = await self.ingredients_repo.get_ingredients_by_recipe_id(recipe.id)
        # print("Here are the ingredients in RecipeServices line 135 -->",ingredients)
        steps = await self.steps_repo.get_step_descriptions_by_recipe_id(recipe.id)
        # print("Here are the steps in RecipeServices line 135 -->",ingredients)

        recipe_data = {
            "id": recipe.id,
            "title": recipe.title,
            "avg_rating": recipe.avg_rating,
            "cooking_time": recipe.cooking_time,
#             "id": recipe["id"],
#             "title": recipe["title"],
#             "avg_rating": recipe["avg_rating"],
#             "cooking_time": recipe["cooking_time"],
            #The ingredients K:V pair is a list of {} where the K is "ingredient_name" and the value is what is in the ingredient_name row in the database
            "ingredients": [{"ingredient_name": ing.ingredient_name} for ing in ingredients],
            "steps": [{"step_order": step.step_order, "step_description": step.step_description} for step in steps]
        }

        return recipe_data