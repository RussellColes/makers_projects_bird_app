import pytest
from lib.models.ingredients import Ingredient
from lib.repositories.ingredients_repo import IngredientRepository
from freezegun import freeze_time

# get ingredients by recipe_id
@pytest.mark.asyncio
async def test_get_ingredients_by_recipe_id(db_connection):
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    repository = IngredientRepository(db_connection)
    result = await repository.get_ingredients_by_recipe_id(1)
    assert len(result) == 11
    assert result[0].ingredient_name == '4 boneless, skinless flamingo breasts'

# create ingredient
@pytest.mark.asyncio
@freeze_time("2024-12-25")
async def test_create_new_ingredient(db_connection):
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    repository = IngredientRepository(db_connection)

    # add new bird sighting into bird_sightings table
    await db_connection.execute(
        'INSERT INTO bird_sightings (id, bird_name, date_spotted, location, user_id) VALUES ($1, $2, $3, $4, $5)',
        [5, "Test bird", None, "Dulwich", 1]
    )

    # add new bird recipe into bird_recipes table
    await db_connection.execute(
        'INSERT INTO bird_recipes (id, title, date_created, recipe_rating, cooking_time, bird_sighting_id) VALUES ($1, $2, $3, $4, $5, $6)',
        [5, "Test Recipe Title", "2024-12-25", 5, 90, 5]
    )

    new_ingredient = Ingredient(None, 5, 'Test ingredient')
    await repository.create_new_ingredient(new_ingredient)
    
    result = await repository.get_ingredients_by_recipe_id(5)
    assert len(result) == 1
    assert result[0].recipe_id == 5
    assert result[0].ingredient_name == 'Test ingredient'


# delete ingredient
