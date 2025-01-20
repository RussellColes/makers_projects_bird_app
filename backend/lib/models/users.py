class User:

    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.profile_picture = 'uploads/default_bird_image.png'


    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "profile_picture": self.profile_picture
            }
        
    def __str__(self):
        return f"User({self.id}, {self.username}, {self.email}, {self.password}, {self.profile_picture})"

    def __repr__(self):
        return f"User({self.id}, {self.username}, {self.email}, {self.password}, {self.profile_picture})"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return (self.id == other.id and
                self.username == other.username and
                self.email == other.email and
                self.profile_picture == other.profile_picture)