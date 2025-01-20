import pytest
from lib.models.sightings import Sighting
from lib.models.ingredients import Ingredient
from lib.models.steps import Step
from unittest.mock import AsyncMock, MagicMock 
import random
from lib.services.RecipeServices import RecipeService
from lib.recipe_templates.recipe_templetes import *

@pytest.fixture
def recipe_choices():
    return [
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
        LASAGNE_RECIPE
    ]

@pytest.fixture
def bird_template():
    """Fixture for a sample bird recipe template."""
    return {
        "title": "Herb-Glazed {BIRD}",
        "cooking_time": 25,
        "ingredients": [
            {"ingredient_name": "4 boneless, skinless {BIRD} breasts."},
            {"ingredient_name": "1 cup {BIRD} broth."}
        ],
        "steps": [
            {"step_order": 1, "step_description": "Prepare the {BIRD}: Pat {BIRD} breasts dry."},
            {"step_order": 2, "step_description": "Cook the {BIRD}: Heat oil in a skillet and add {BIRD}."}
        ]
    }


def test_select_random_recipe_returns_valid_recipe(recipe_choices):
    """
    Test that select_random_recipe() returns a recipe from the predefined list.
    """
    selected_recipe = RecipeService.select_random_recipe()
    assert selected_recipe in recipe_choices, "The selected recipe is not in the list of recipe choices."

def test_selected_recipe_structure():
    """
    Test that the selected recipe has the correct structure (keys: title, cooking_time, ingredients, steps).
    """
    selected_recipe = RecipeService.select_random_recipe()
    assert "title" in selected_recipe, "Recipe is missing the 'title' key."
    assert "cooking_time" in selected_recipe, "Recipe is missing the 'cooking_time' key."
    assert "ingredients" in selected_recipe, "Recipe is missing the 'ingredients' key."
    assert "steps" in selected_recipe, "Recipe is missing the 'steps' key."
    assert isinstance(selected_recipe["ingredients"], list), "'ingredients' should be a list."
    assert isinstance(selected_recipe["steps"], list), "'steps' should be a list."

def test_populate_bird_template_replaces_bird_name(bird_template):
    """
    Test that _populate_bird_template replaces '{BIRD}' with the provided bird_name.
    """
    service = RecipeService(None, None, None, None, None)
    bird_name = "Flamingo"
    populated_recipe = service._populate_bird_template(bird_template, bird_name)
    
    assert populated_recipe["title"] == "Herb-Glazed Flamingo", "Title was not populated correctly."
    
    # Check ingredients
    assert populated_recipe["ingredients"][0]["ingredient_name"] == "4 boneless, skinless Flamingo breasts."
    assert populated_recipe["ingredients"][1]["ingredient_name"] == "1 cup Flamingo broth."
    
    # Check steps
    assert populated_recipe["steps"][0]["step_description"] == "Prepare the Flamingo: Pat Flamingo breasts dry."
    assert populated_recipe["steps"][1]["step_description"] == "Cook the Flamingo: Heat oil in a skillet and add Flamingo."

def test_populate_bird_template_maintains_structure(bird_template):
    """
    Test that _populate_bird_template maintains the structure of the template.
    """
    service = RecipeService(None, None, None, None, None)
    bird_name = "duck"
    populated_recipe = service._populate_bird_template(bird_template, bird_name)
    
    assert "title" in populated_recipe, "'title' key is missing in the populated recipe."
    assert "cooking_time" in populated_recipe, "'cooking_time' key is missing in the populated recipe."
    assert "ingredients" in populated_recipe, "'ingredients' key is missing in the populated recipe."
    assert "steps" in populated_recipe, "'steps' key is missing in the populated recipe."

    # Check types
    assert isinstance(populated_recipe["ingredients"], list), "'ingredients' is not a list."
    assert isinstance(populated_recipe["steps"], list), "'steps' is not a list."
    assert isinstance(populated_recipe["steps"][0]["step_order"], int), "'step_order' should be an integer."

def test_populate_bird_template_with_multiple_bird_names(bird_template):
    """
    Test _populate_bird_template with different bird names to ensure consistent behavior.
    """
    service = RecipeService(None, None, None, None, None)
    
    for bird_name in ["Flamingo", "turkey", "duck"]:
        populated_recipe = service._populate_bird_template(bird_template, bird_name)
        assert bird_name in populated_recipe["title"], f"'{bird_name}' was not replaced in the title."
        assert bird_name in populated_recipe["ingredients"][0]["ingredient_name"], f"'{bird_name}' was not replaced in ingredients."
        assert bird_name in populated_recipe["steps"][0]["step_description"], f"'{bird_name}' was not replaced in steps."

@pytest.mark.asyncio
async def test_create_recipe_from_bird_name_success():
    # Arrange
    bird_name = "Flamingo"
    user_id = 3
    sighting_id = 1
    recipe_id = 1

    # Mock repositories
    mock_sightings_repo = MagicMock()
    mock_sightings_repo.create_bird_sighting = AsyncMock(return_value=sighting_id)

    mock_recipes_repo = MagicMock()
    mock_recipes_repo.create_recipe = AsyncMock(return_value=recipe_id)

    mock_ingredients_repo = MagicMock()
    mock_ingredients_repo.create_new_ingredient = AsyncMock()

    mock_steps_repo = MagicMock()
    mock_steps_repo.create_new_step = AsyncMock()

    # Mock RecipeService dependencies
    service = RecipeService(
        sightings_repo=mock_sightings_repo,
        recipes_repo=mock_recipes_repo,
        ingredients_repo=mock_ingredients_repo,
        steps_repo=mock_steps_repo,
        connection=None
    )

    # Mock internal methods
    service.select_random_recipe = MagicMock(return_value={
        "title": "Herb-Glazed {BIRD}",
        "cooking_time": 25,
        "ingredients": [{"ingredient_name": "4 boneless, skinless {BIRD} breasts."}],
        "steps": [{"step_order": 1, "step_description": "Prepare the {BIRD}."}]
    })
    service._populate_bird_template = MagicMock(return_value={
        "title": "Herb-Glazed Flamingo",
        "cooking_time": 25,
        "ingredients": [{"ingredient_name": "4 boneless, skinless Flamingo breasts."}],
        "steps": [{"step_order": 1, "step_description": "Prepare the Flamingo."}]
    })

    # Act
    result = await service.create_recipe_from_bird_name(bird_name, user_id)

    # Assert
    assert result == recipe_id, "The returned recipe_id does not match the expected value."

    # Verify Sighting was created
    mock_sightings_repo.create_bird_sighting.assert_called_once_with(
        Sighting(None, bird_name, None, None, user_id)
    )

    # Verify Recipe was created
    mock_recipes_repo.create_recipe.assert_called_once()
    created_recipe = mock_recipes_repo.create_recipe.call_args[0][0]
    assert created_recipe.title == "Herb-Glazed Flamingo"
    assert created_recipe.cooking_time == 25

    # Verify Ingredients were added
    mock_ingredients_repo.create_new_ingredient.assert_called_once_with(
        Ingredient(None, recipe_id, "4 boneless, skinless Flamingo breasts.")
    )

    # Verify Steps were added
    mock_steps_repo.create_new_step.assert_called_once_with(
        Step(None, recipe_id, 1, "Prepare the Flamingo.")
    )

@pytest.mark.asyncio
async def test_create_recipe_from_bird_name_failure():
    # Arrange
    bird_name = "turkey"
    user_id = 456

    # Mock repositories with failure
    mock_sightings_repo = MagicMock()
    mock_sightings_repo.create_bird_sighting = AsyncMock(return_value=None)  # Simulate failure

    # Service instance
    service = RecipeService(
        sightings_repo=mock_sightings_repo,
        recipes_repo=MagicMock(),
        ingredients_repo=MagicMock(),
        steps_repo=MagicMock(),
        connection=None
    )

    # Act
    result = await service.create_recipe_from_bird_name(bird_name, user_id)

    # Assert
    assert result is None, "The result should be None on failure."
    mock_sightings_repo.create_bird_sighting.assert_called_once()