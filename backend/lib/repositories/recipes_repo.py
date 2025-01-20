from lib.models.recipes import Recipe
import datetime

class RecipeRepository():
        
        def __init__(self, connection): #require database connection when UserRepository object is created
            self._connection = connection

        async def get_all_recipes(self):
            query = """
                SELECT 
                    bird_recipes.id, 
                    bird_recipes.title, 
                    bird_recipes.date_created, 
                    bird_recipes.cooking_time, 
                    bird_recipes.bird_sighting_id,
                    get_avg_recipe_rating(bird_recipes.id) AS avg_rating
                FROM bird_recipes
                ORDER BY bird_recipes.id
            """
            rows = await self._connection.execute(query)
            recipes = []
            for row in rows:
                recipe = Recipe(
                    row["id"],
                    row["title"], 
                    row["date_created"],
                    row["cooking_time"],
                    row["bird_sighting_id"],
                    row["avg_rating"]
                )
                recipes.append(recipe)
            return recipes    

        async def get_single_recipe(self, sighting_id):
            query = """
                SELECT 
                    bird_recipes.id, 
                    bird_recipes.title, 
                    bird_recipes.date_created, 
                    bird_recipes.cooking_time, 
                    bird_recipes.bird_sighting_id,
                    get_avg_recipe_rating(bird_recipes.id) AS avg_rating
                FROM bird_recipes
                WHERE bird_recipes.bird_sighting_id = $1
            """
            rows = await self._connection.execute(query, [sighting_id])
            if not rows:
                return None  # Return None if no recipe is found
            row = rows[0]

            return Recipe(
                row["id"], 
                row["title"], 
                row["date_created"], 
                row["cooking_time"], 
                row["bird_sighting_id"], 
                row["avg_rating"]
            )
        
        async def create_recipe(self, recipe):
            date_spotted = datetime.datetime.now().date().strftime('%Y-%m-%d')
        # This validation might be handles in the schema files later (not sure yet)
            # if not recipe.title:
            #     return 'Please provide a title'
            # if not recipe.date_created:
            #     return 'Please provide a date created'
            # if not recipe.cooking_time:
            #     return 'Please provide a cooking time'
            # if not recipe.bird_sighting_id:
            #     return 'Please provide a bird_sighting id'
            result = await self._connection.fetch(
                '''
                INSERT INTO bird_recipes (title, date_created, cooking_time, bird_sighting_id)
                VALUES ($1, $2, $3, $4)
                RETURNING id
                ''',
                [recipe.title, date_spotted, recipe.cooking_time, recipe.bird_sighting_id])
            id = result[0]['id']
            print("recipe id --->", id)
            return id
        
        async def update_recipe_title(self, id, title):
            await self._connection.execute(
                'UPDATE bird_recipes SET title = $1 WHERE id = $2', 
                [title, id])
            return None
        
        async def update_recipe_cooking_time(self, id, cooking_time):
            await self._connection.execute(
                'UPDATE bird_recipes SET cooking_time = $1 WHERE id = $2', 
                [cooking_time, id])
            return None
        
        async def delete_recipe(self, id):
            await self._connection.execute(
                'DELETE FROM bird_recipes WHERE id = $1', [id])
            return None
        

# OLD FUNCTIONS BELOW BEFORE AVERAGE RATINGS NONSENSE:

        # async def get_all_recipes(self):
        #     rows = await self._connection.execute('SELECT * FROM bird_recipes ORDER BY id')
        #     recipes = []
        #     for row in rows:
        #         recipe = Recipe(row["id"], row["title"], row["date_created"], row["cooking_time"], row["bird_sighting_id"])
        #         recipes.append(recipe)
        #     return recipes


        # async def get_single_recipe(self, id):
        #     rows = await self._connection.execute(
        #         'SELECT * FROM bird_recipes WHERE id = $1', [id])
        #     if not rows:
        #         return None  # Return None if no recipe is found
        #     row = rows[0]
        #     return Recipe(row["id"], row["title"], row["date_created"], row["cooking_time"], row["bird_sighting_id"], row["avg_rating"])