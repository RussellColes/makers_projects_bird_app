from lib.models.ratings import Rating

"""
Rating constructs
"""
def test_ingredients_constructs():
    rating = Rating(1, 5, 2)
    assert rating.id == 1
    assert rating.rating_score == 5
    assert rating.recipe_id == 2

def test_recipe_to_dict():
    rating = Rating(1, 5, 2)
    expected_dict = {
    "id": 1,
    "rating_score": 5,
    "recipe_id": 2
    }
    assert rating.to_dict() == expected_dict

"""
We can format ratings to strings nicely
"""
def test_ingredient_format_nicely():
    rating = Rating(1, 5, 2)
    assert str(rating) == 'Rating(1, 5, 2)'

"""
We can compare two identical ratings
And have them be equal
"""
def test_ingredients_are_equal():
    Rating1 = Rating(1, 1, 'Potatoes')
    Rating2 = Rating(1, 1, 'Potatoes')
    assert Rating1 == Rating2