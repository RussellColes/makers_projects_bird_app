import pytest
from lib.models.recipes import Recipe
from lib.repositories.recipes_repo import RecipeRepository
from freezegun import freeze_time

@pytest.mark.asyncio
async def test_get_all_recipes(db_connection):
    # Seed the database with the provided SQL file
    await db_connection.seed('lib/db/seeds/birdfood_app.sql') 
    # Instantiate the repository and call the method
    repository = RecipeRepository(db_connection)
    result = await repository.get_all_recipes()
    # Define the expected result based on the seed data
    expected_result = [
        Recipe(1, 'Herb-Glazed Flamingo', '2024-12-01', 25, 1, 5.0), 
        Recipe(2, 'Hearty Winter Woodpecker Pie', '2024-12-01', 40, 2, 3.5),
        Recipe(3, 'Jamaican Jerk Peregrine Falcon', '2024-12-01', 40, 3, 4.0),
        Recipe(4, 'Twice-Fried Resplendent Quetzal Wings', '2024-12-01', 20, 4, 3.5) 
    ]
    # Assert that the result matches the expected result
    assert result == expected_result

@pytest.mark.asyncio
async def test_get_single_recipe(db_connection):
    # Seed the database with the provided SQL file
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    # Instantiate the repository and call the method for a single recipe
    repository = RecipeRepository(db_connection)
    result = await repository.get_single_recipe(1)
    # Define the expected result for recipe with ID 1
    expected_result = Recipe(1, 'Herb-Glazed Flamingo', '2024-12-01', 25, 1, 5.0)
    # Assert that the result matches the expected result
    assert result == expected_result

@pytest.mark.asyncio
@freeze_time("2024-12-01")
async def test_create_new_recipe(db_connection):
    # Seed the database with the provided SQL file
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    # Instantiate the repository
    repository = RecipeRepository(db_connection)
    # Create a new recipe
    # Add new recipe to database
    await repository.create_recipe(Recipe(None, 'Test recipe', '2024-12-01', 25, 4, None))
    # Retrieve all recipes to check if the new recipe was added
    result = await repository.get_all_recipes()
    # Define the expected result based on the seed data
    assert len(result) == 5
    assert result == [
        Recipe(1, 'Herb-Glazed Flamingo', '2024-12-01', 25, 1, 5.0), 
        Recipe(2, 'Hearty Winter Woodpecker Pie', '2024-12-01', 40, 2, 3.5),
        Recipe(3, 'Jamaican Jerk Peregrine Falcon', '2024-12-01', 40, 3, 4.0),
        Recipe(4, 'Twice-Fried Resplendent Quetzal Wings', '2024-12-01', 20, 4, 3.5),
        Recipe(5, 'Test recipe', '2024-12-01', 25, 4, None) 
    ]

@pytest.mark.asyncio
async def test_update_recipe_title(db_connection):
    # Seed the database with the provided SQL file
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    # Instantiate the repository
    repository = RecipeRepository(db_connection)
    # Update the title of the recipe with ID 1
    await repository.update_recipe_title(1, 'Blue Jay Supreme')
    # Fetch the updated recipe
    updated_recipe = await repository.get_single_recipe(1)
    # Assert that the title has been updated
    assert updated_recipe.title == 'Blue Jay Supreme'

@pytest.mark.asyncio
async def test_update_recipe_cooking_time(db_connection):
    # Seed the database with the provided SQL file
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    # Instantiate the repository
    repository = RecipeRepository(db_connection)
    # Update the cooking time of the recipe with ID 1
    await repository.update_recipe_cooking_time(1, 50)
    # Fetch the updated recipe
    updated_recipe = await repository.get_single_recipe(1)
    # Assert that the title has been updated
    assert updated_recipe.cooking_time == 50

@pytest.mark.asyncio
async def test_delete_recipe(db_connection):
    # Seed the database with the provided SQL file
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    # Instantiate the repository
    repository = RecipeRepository(db_connection)
    # Delete the recipe with ID 1
    await repository.delete_recipe(1)
    # Try to fetch the deleted recipe
    deleted_recipe = await repository.get_single_recipe(1)
    # Assert that the recipe no longer exists
    assert deleted_recipe is None