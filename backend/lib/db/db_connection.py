import os, asyncpg
from flask import g

# This class helps us interact with the database.
# It wraps the underlying asyncpg library that we are using.

class AsyncDatabaseConnection:
    # VVV CHANGE BOTH OF THESE VVV
    DEV_DATABASE_NAME = "birdfood_project"
    TEST_DATABASE_NAME = "birdfood_project_test"

    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.connection = None

    # This method connects to PostgreSQL using the asyncpg library. We connect
    # to localhost and select the database name given in argument.
    async def connect(self):
        try:
            self.connection = await asyncpg.connect(
                f"postgresql://localhost/{self._database_name()}"
                )
            print("Made connection to database", self._database_name())
        except asyncpg.PostgresError:
            raise Exception(f"Couldn't connect to the database {self._database_name()}! " \
                    f"Did you create it using `createdb {self._database_name()}`?")

    # This method seeds the database with the given SQL file.
    # We use it to set up our database ready for our tests or application.
    async def seed(self, sql_filename):
        await self._check_connection()
        if not os.path.exists(sql_filename):
            raise Exception(f"File {sql_filename} does not exist")
        with open(sql_filename, "r") as file:
            sql = file.read()
        await self.connection.execute(sql)

    # This method executes an SQL query on the database.
    # It allows you to set some parameters too. You'll learn about this later.
    async def execute(self, query, params=[]):
        await self._check_connection()
        try:
            if query.strip().upper().startswith("SELECT"):
                result = await self.connection.fetch(query, *params)
            else:
                result = await self.connection.execute(query, *params)
            return result
        except asyncpg.PostgresError as e:
            raise Exception(f"Database query failed: {e}")

    CONNECTION_MESSAGE = '' \
        'DatabaseConnection.exec_params: Cannot run a SQL query as ' \
        'the connection to the database was never opened. Did you ' \
        'make sure to call first the method DatabaseConnection.connect` ' \
        'in your app.py file (or in your tests)?'
    
    async def fetch(self, query, params=[]):
        await self._check_connection()
        try:
            result = await self.connection.fetch(query, *params)
            return result
        except asyncpg.PostgresError as e:
            raise Exception(f"Database query (fetch) failed: {e}")

    # This private method checks that we're connected to the database.
    async def _check_connection(self):
        if self.connection is None:
            raise Exception(self.CONNECTION_MESSAGE)

    # This private method returns the name of the database we should use.
    def _database_name(self):
        if self.test_mode:
            return self.TEST_DATABASE_NAME
        else:
            return self.DEV_DATABASE_NAME

# This function integrates with Flask to create one database connection that
# Flask request can use. To see how to use it, look at example_routes.py
async def get_flask_database_connection(app):
    if not hasattr(g, 'flask_database_connection'):
        g.flask_database_connection = AsyncDatabaseConnection(
            test_mode=((os.getenv('APP_ENV') == 'test') or (app.config['TESTING'] == True))
        )

        # print("get flask database")
        # print(dir(g.flask_database_connection))
        await g.flask_database_connection.connect()

    # print(g.flask_database_connection)
    return g.flask_database_connection

