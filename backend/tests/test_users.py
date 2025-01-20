from lib.models.users import User

"""
User constructs with an username, email and password
"""
def test_user_constructs():
    user = User(1, "bird_lover", "birdlover@email.com", "password123")
    assert user.id == 1
    assert user.username == "bird_lover"
    assert user.email == "birdlover@email.com"
    assert user.password == "password123"
#     assert user.verify_password("password123")
#     assert user.password == "password123"
    assert user.profile_picture == "uploads/default_photo.webp"


def test_recipe_to_dict():
    user = User(1, "bird_lover", "birdlover@email.com", "password123")
    expected_dict = {
    "id": 1,
    "username": 'bird_lover',
    "email": 'birdlover@email.com',
    "profile_picture": 'uploads/default_photo.webp'
    }
    assert user.to_dict() == expected_dict

"""
We can format users to strings nicely
"""
def test_user_format_nicely():
    user = User(1, "bird_lover", "birdlover@email.com", "password123")
    assert str(user) == "User(1, bird_lover, birdlover@email.com, password123, uploads/default_photo.webp)"

"""
We can compare two identical users
And have them be equal
"""
def test_users_are_equal():
    user1 = User(1, "bird_lover", "birdlover@email.com", "password123")
    user2 = User(1, "bird_lover", "birdlover@email.com", "password123")
    assert user1 == user2

