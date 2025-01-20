from lib.models.steps import Step

"""
Step constructs
"""
def test_steps_constructs():
    user = Step(1, 1, 1, 'Peel potatoes')
    assert user.id == 1
    assert user.recipe_id == 1
    assert user.step_order == 1
    assert user.step_description == "Peel potatoes"

def test_recipe_to_dict():
    user = Step(1, 1, 1, 'Peel potatoes')
    expected_dict = {
    "id": 1,
    "recipe_id": 1,
    "step_order": 1,
    "step_description": 'Peel potatoes'
    }
    assert user.to_dict() == expected_dict

"""
We can format users to strings nicely
"""
def test_step_format_nicely():
    steps = Step(1, 1, 1, 'Peel potatoes')
    assert str(steps) == 'Step(1, 1, 1, Peel potatoes)'


"""
We can compare two identical users
And have them be equal
"""
def test_steps_are_equal():
    Steps1 = Step(1, 1, 1, 'Peel potatoes')
    Steps2 = Step(1, 1, 1, 'Peel potatoes')
    assert Steps1 == Steps2