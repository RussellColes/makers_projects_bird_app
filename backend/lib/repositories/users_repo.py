from lib.models.users import User
from lib.utils.password_utils import *

class UserRepository():
    def __init__(self, connection): #require database connection when UserRepository object is created
        self._connection = connection

    async def get_all_users(self):
        rows = await self._connection.execute('SELECT * FROM users ORDER BY id')
        users = []
        for row in rows:
            user = User(row["id"], row["username"], row["email"], row["password"])
            users.append(user)
        return users


    async def get_single_user_by_id(self, id):
        rows = await self._connection.execute(
            'SELECT * FROM users WHERE id = $1', [id])
        if len(rows) == 0:
            return None
        else:
            row = rows[0]
            return User(row["id"], row["username"], row["email"], row["password"])

    async def get_single_user_by_email(self, email):
        rows = await self._connection.execute(
            'SELECT * FROM users WHERE email = $1', [email])
        if len(rows) == 0:
            return None
        else:
            row = rows[0]
            return User(row["id"], row["username"], row["email"], row["password"])


    async def get_single_user_by_username(self, username):
        rows = await self._connection.execute(
            'SELECT * FROM users WHERE username = $1', [username])
        if len(rows) == 0:
            return None
        else:
            row = rows[0]
            return User(row["id"], row["username"], row["email"], row["password"])


    # async def create_user(self, user):
        # This validation might be handles in the schema files later (not sure yet)
        # if not user.username:
        #     return 'Please provide a username'
        # if not user.email:
        #     return 'Please provide an email address'
        # if not user.password:
        #     return 'Please provide a password'
        
    async def create_user(self, user):
        hashed_password = hash_password(user.password)
        await self._connection.execute(
            'INSERT INTO users (username, email, password, profile_picture) VALUES ($1, $2, $3, $4)',
            [user.username, user.email, hashed_password, user.profile_picture])
        # else:
        #     await self._connection.execute(
        #         'INSERT INTO users (username, email, password, profile_picture) VALUES ($1, $2, $3, $4)',
        #         [user.username, user.email, user.password, user.profile_picture])
        return None

    async def update_user_password(self, id, password):
        await self._connection.execute(
            'UPDATE users SET password = $1 WHERE id = $2', 
            [password, id])
        return None

    async def update_user_email(self, id, email):
        await self._connection.execute(
            'UPDATE users SET email = $1 WHERE id = $2', 
            [email, id])
        return None

    async def update_user_username(self, id, username):
        await self._connection.execute(
            'UPDATE users SET username = $1 WHERE id = $2', 
            [username, id])
        return None

    async def delete_user(self, id):
        await self._connection.execute(
            'DELETE FROM users WHERE id = $1',
            [id]
        )
        return None

    async def update_user_picture(self, picture_filepath, user_id):
        await self._connection.execute(
            'UPDATE users SET profile_picture = $1 WHERE id = $2', [picture_filepath, user_id])
        return None
    
    async def validate_user(self, payload):
        rows = await self._connection.execute(
            'SELECT * FROM users WHERE email = $1', 
            [payload["email"]])
        if len(rows) == 0:
            return False
        user = rows[0]
        stored_hashed_password = user["password"]
        return verify_password(stored_hashed_password, payload["password"])
