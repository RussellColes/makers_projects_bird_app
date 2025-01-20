from lib.models.sightings import Sighting
import datetime

class SightingRepository():
    def __init__(self, connection):
        self._connection = connection

    # get all sightings
    async def get_all_sightings(self):
        rows = await self._connection.execute('SELECT * FROM bird_sightings ORDER BY id')
        sightings = []
        print("Here's the list of sightings from line 11 -->", sightings)
        for row in rows:
            sighting = Sighting(row["id"], row["bird_name"], row["date_spotted"], row["location"], row["image"], row["user_id"])
            sightings.append(sighting)
        return sightings

    # get single sighting by id
    async def get_sighting_by_id(self, id):
        int_id = int(id)
        print("here is the integer id on line 20", int_id)
        sightings = await self._connection.execute(
            'SELECT * FROM bird_sightings WHERE id = $1', [int_id]
            )
        print("sightings line 24", sightings)
        if not sightings:
            return None
        else:
            sighting = sightings[0]
            return Sighting(sighting["id"], sighting["bird_name"], sighting["date_spotted"], sighting["location"], sighting["image"], sighting["user_id"]  )

    # get all sightings by location
    async def get_sightings_by_location(self, location):
        rows = await self._connection.execute(
            'SELECT * FROM bird_sightings WHERE location = $1', [location]
        )
        sightings = []
        if not rows:
            return None
        else: 
            for row in rows:
                sighting = Sighting(row["id"], row["bird_name"], row["date_spotted"], row["location"], row["image"], row["user_id"])
                sightings.append(sighting)
            return sightings
            
    # get all sightings by date_spotted
    async def get_sightings_by_date_spotted(self, date_spotted):
        rows = await self._connection.execute(
            'SELECT * FROM bird_sightings WHERE date_spotted = $1', [date_spotted]
        )
        sightings = []
        if not rows:
            return None
        else:
            for row in rows:
                sighting = Sighting(row["id"], row["bird_name"], row["date_spotted"], row["location"], row["image"], row["user_id"])
                sightings.append(sighting)
            return sightings

    # get all sightings by bird_name
    async def get_sightings_by_bird_name(self, bird_name):
        rows = await self._connection.execute(
            'SELECT * FROM bird_sightings WHERE bird_name = $1', [bird_name]
        )
        sightings = []
        if not rows:
            return None
        else:
            for row in rows:
                sighting = Sighting(row["id"], row["bird_name"], row["date_spotted"], row["location"], row["image"], row["user_id"])
                sightings.append(sighting)
            return sightings


    # get all sightings by user_id
    async def get_sightings_by_user_id(self, user_id):
        print("this is user id in sightings repo line 77 -->", user_id)
        rows = await self._connection.execute(
            'SELECT * FROM bird_sightings WHERE user_id = $1', [user_id]
        )
        print("this is rows in sightings repo line 81 -->", rows)
        sightings = []
        if not rows:
            return None
        else:
            for row in rows:
                sighting = Sighting(row["id"], row["bird_name"], row["date_spotted"], row["location"], row["image"], row["user_id"])
                sightings.append(sighting)
            print("this is sightings in sightings repo line 89 -->", sightings)
            return sightings if len(sightings) > 0 else None

    # create bird_sighting
    async def create_bird_sighting(self, sighting):
        date_spotted = datetime.datetime.now().date().strftime('%Y-%m-%d')

        result = await self._connection.fetch(
            '''
            INSERT INTO bird_sightings (bird_name, date_spotted, location, image, user_id)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
            ''',
            [sighting.bird_name, date_spotted, sighting.location, sighting.image, sighting.user_id])
        id = result[0]['id']
        print('sightings_repo line 97 - sightings_id', id)
        return id

    # delete bird sighting
    async def delete_bird_sighting(self, id):
        await self._connection.execute(
            'DELETE FROM bird_sightings WHERE id = $1', [id]
        )
        return None