from lib.models.ratings import Rating

class RatingRepository:
    def __init__(self, connection):
        self._connection = connection

    async def get_all_ratings(self):
        rows = await self._connection.execute('SELECT * FROM ratings ORDER BY id')
        ratings = []
        for row in rows:
            rating = Rating(
                id=row["id"],
                rating_score=row["rating_score"],
                recipe_id=row["recipe_id"]
            )
            ratings.append(rating)
        return ratings

    async def get_rating_by_id(self, id):
        rows = await self._connection.execute(
            'SELECT * FROM ratings WHERE id = $1', [id]
        )
        if not rows:
            return None
        row = rows[0]
        return Rating(
            id=row["id"],
            rating_score=row["rating_score"],
            recipe_id=row["recipe_id"]
        )

    async def get_ratings_for_recipe(self, recipe_id):
        rows = await self._connection.execute(
            'SELECT * FROM ratings WHERE recipe_id = $1', [recipe_id]
        )
        ratings = []
        for row in rows:
            rating = Rating(
                id=row["id"],
                rating_score=row["rating_score"],
                recipe_id=row["recipe_id"]
            )
            ratings.append(rating)
        return ratings

    async def create_rating(self, rating):
        rating_id = await self._connection.execute(
            '''
            INSERT INTO ratings (rating_score, recipe_id)
            VALUES ($1, $2)
            RETURNING id
            ''',
            [rating.rating_score, rating.recipe_id]
        )
        return rating_id

    async def update_rating_score(self, id, rating_score):
        await self._connection.execute(
            '''
            UPDATE ratings
            SET rating_score = $1
            WHERE id = $2
            ''',
            [rating_score, id]
        )
        return None

    async def delete_rating(self, id):
        await self._connection.execute(
            'DELETE FROM ratings WHERE id = $1', [id]
        )
        return None
