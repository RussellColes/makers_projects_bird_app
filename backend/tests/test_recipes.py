from lib.models.recipes import Recipe

def test_recipe_constructs():
    recipe = Recipe(1, 'Blue Jay Roast', '2024-12-01', 45, 1, avg_rating=5)
    assert recipe.id == 1
    assert recipe.title == 'Blue Jay Roast'
    assert recipe.date_created == '2024-12-01'
    assert recipe.cooking_time == 45
    assert recipe.bird_sighting_id == 1
    assert recipe.avg_rating == 5

def test_recipe_to_dict():
    recipe = Recipe(1, 'Blue Jay Roast', '2024-12-01', 45, 1, avg_rating=5)
    expected_dict = {
        "id": 1,
        "title": 'Blue Jay Roast',
        "date_created": '2024-12-01',
        "cooking_time": 45,
        "bird_sighting_id": 1,
        "avg_rating": 5
    }
    assert recipe.to_dict() == expected_dict

def test_recipe_formats_nicely():
    recipe = Recipe(1, 'Blue Jay Roast', '2024-12-01', 45, 1, avg_rating=5)
    assert str(recipe) == "Recipe(1, Blue Jay Roast, 2024-12-01, 45, 1, 5)"

def test_recipes_are_equal():
    recipe1 = Recipe(1, 'Blue Jay Roast', '2024-12-01', 45, 1, avg_rating=5)
    recipe2 = Recipe(1, 'Blue Jay Roast', '2024-12-01', 45, 1, avg_rating=5)
    assert recipe1 == recipe2