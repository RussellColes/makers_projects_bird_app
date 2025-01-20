import pytest
from lib.models.steps import Step
from lib.repositories.steps_repo import StepRepository
from freezegun import freeze_time

# get all steps --> I don't see why would need this

# get single step by id
@pytest.mark.asyncio
async def test_get_single_step_by_id(db_connection):
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    repository = StepRepository(db_connection)
    result = await repository.get_single_step_by_id(3)
    assert result.recipe_id == 1
    assert result.step_order == 3

# get step_descriptions by recipe_id
@pytest.mark.asyncio
async def test_get_step_descriptions_by_recipe_id(db_connection):
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    repository = StepRepository(db_connection)
    result = await repository.get_step_descriptions_by_recipe_id(3)
    assert result == [
        Step(13, 3, 1, 'In a blender or food processor, combine the Scotch bonnets, spring onions, garlic, thyme, allspice, brown sugar, soy sauce, lime juice, and oil. Blend until a thick, smooth paste forms. Season with salt and pepper.'),
        Step(14, 3, 2, 'Place the peregrine falcon pieces in a large bowl or zip-top bag. Pour over the jerk marinade, ensuring all pieces are well coated. Marinate for at least 4 hours, ideally overnight.'),
        Step(15, 3, 3, 'Preheat a grill (or oven to 200°C/400°F).'),
        Step(16, 3, 4, 'Grill the marinated peregrine falcon over medium heat until well-browned, slightly charred, and cooked through (juices run clear, internal temperature of 75°C/165°F), about 40-45 minutes. If using the oven, place the peregrine falcon on a baking tray and roast until fully cooked, turning occasionally for even browning.'),
        Step(17, 3, 5, 'Let the peregrine falcon rest for a few minutes before serving with rice and peas, plantains, or a fresh salad.'),
    ]

# create step
@pytest.mark.asyncio
@freeze_time("2024-12-25")
async def test_create_new_step(db_connection):
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    repository = StepRepository(db_connection)

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

    new_step = Step(None, 5, 1, 'Test recipe step')
    await repository.create_new_step(new_step)
    
    result = await repository.get_step_descriptions_by_recipe_id(5)
    assert len(result) == 1
    assert result[0].recipe_id == 5
    assert result[0].step_order == 1
    assert result[0].step_description == 'Test recipe step'

# delete step
# @pytest.mark.asyncio
# async def test_delete_step(db_connection):
#     await db_connection.seed('lib/db/seeds/birdfood_app.sql')
#     repository = StepRepository(db_connection)
#     await repository.delete_step(2)
#     remaining_steps = await repository.get_step_descriptions_by_recipe_id(4)
#     assert len(remaining_steps) == 4
#     assert remaining_steps[-1].recipe_id == 4
#     assert remaining_steps[-2].step_order == 3
