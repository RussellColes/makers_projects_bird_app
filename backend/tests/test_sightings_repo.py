import pytest #needs to be imported to allow for @pytest.mark.asyncho decorator
from lib.models.sightings import Sighting
from lib.repositories.sightings_repo import SightingRepository
from freezegun import freeze_time


"""
When we call get_all_sightings()
We get a list of Sighting objects reflecting the seed data.
"""

@pytest.mark.asyncio
async def test_get_all_sightings(db_connection):
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    repository = SightingRepository(db_connection)
    result = await repository.get_all_sightings()
    assert result == [
        Sighting(1, 'Flamingo', '2024-12-01', 'Shoreditch', None, 1),
        Sighting(2, 'Woodpecker', '2024-12-01', 'Peckham', None, 2),
        Sighting(3, 'Peregrine Falcon', '2024-12-01', 'Wimbledon', None, 3),
        Sighting(4, 'Resplendent Quetzal', '2024-12-01', 'Greenwich', None, 3)
    ]

    # get single sighting by id
"""
When we call get_sighting_by_id()
We get a Sighting object with that id
"""
@pytest.mark.asyncio
async def test_get_sighting_by_id(db_connection):
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    repository = SightingRepository(db_connection)
    result = await repository.get_sighting_by_id(2)
    assert result == Sighting(2, 'Woodpecker', '2024-12-01', 'Peckham', None, 2)

"""
When we call get_sighting_by_id() but no sighting exists
We get an error message
"""
@pytest.mark.asyncio
async def test_get_sighting_by_id_where_none_exist(db_connection):
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    repository = SightingRepository(db_connection)
    result = await repository.get_sighting_by_id(5)
    assert result is None

    # get all sightings by location
"""
When we call get_sightings_by_location()
We get a list of Sighting objects from that location.
"""
@pytest.mark.asyncio
async def test_get_sighting_by_location(db_connection):
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    repository = SightingRepository(db_connection)
    result = await repository.get_sightings_by_location("Shoreditch")
    assert len(result) == 1
    assert result[0].location == "Shoreditch"

"""
When we call get_sightings_by_location() but no sighting exists
We get an error message
"""
@pytest.mark.asyncio
async def test_get_sightings_by_bird_location_where_none_exist(db_connection):
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    repository = SightingRepository(db_connection)
    result = await repository.get_sightings_by_location("Leeds")
    assert result is None

    # get all sightings by date_spotted
"""
When we call get_sightings_by_date_spotted()
We get a list of Sighting objects spotted on that date.
"""
@pytest.mark.asyncio
async def test_get_sightings_by_date_spotted(db_connection):
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    repository = SightingRepository(db_connection)
    result = await repository.get_sightings_by_date_spotted('2024-12-01')
    assert len(result) == 4

"""
When we call get_sightings_by_date_spotted()but no sighting exists
We get an error message
"""
@pytest.mark.asyncio
async def test_get_sightings_by_date_spotted_where_none_exist(db_connection):
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    repository = SightingRepository(db_connection)
    result = await repository.get_sightings_by_date_spotted('2023-10-02')
    assert result is None



    # get all sightings by bird_name
"""
When we call get_sightings_by_bird_name()
We get a list of Sighting objects with that bird name.
"""
@pytest.mark.asyncio
async def test_get_sightings_by_bird_name(db_connection):
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    repository = SightingRepository(db_connection)
    result = await repository.get_sightings_by_bird_name("Woodpecker")
    assert len(result) == 1


"""
When we call get_sightings_by_bird_name() but no sighting exists
We get a an error message
"""
@pytest.mark.asyncio
async def test_get_sightings_by_bird_name_where_none_exist(db_connection):
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    repository = SightingRepository(db_connection)
    result = await repository.get_sightings_by_bird_name("Bald Eagle")
    assert result is None


    # get all sightings by user_id
"""
When we call get_sightings_by_user_id()
We get a list of all Sighting objects by that user.
"""
@pytest.mark.asyncio
async def test_get_sighting_by_user_id(db_connection):
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    repository = SightingRepository(db_connection)
    
    result = await repository.get_sightings_by_user_id(3)
    assert len(result) == 2

"""
When we call get_sighting_by_id() but no sighting exists
We get an error message
"""
@pytest.mark.asyncio
async def test_get_sighting_by_user_id_where_none_exist(db_connection):
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    repository = SightingRepository(db_connection)
    result = await repository.get_sightings_by_user_id(5)
    assert result is None

    # create bird_sighting
"""
When we call create_bird_sighting
A new bird_sighting is created and stored in the database
"""
# This test needs to mock the current date --> using feeze_time
@pytest.mark.asyncio
@freeze_time("2024-12-25") #merry christmas
async def test_create_bird_sighting(db_connection):
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    repository = SightingRepository(db_connection)

    new_sighting = Sighting(None, 'test sighting', None, 'East Dulwich', "path/to/image", 1)
    await repository.create_bird_sighting(new_sighting)
        
    sightings = await repository.get_all_sightings()

    assert len(sightings) == 5
    assert sightings[-1].bird_name == 'test sighting'
    assert sightings[-1].date_spotted == '2024-12-25'

    # delete bird sighting
"""
When we call delete_bird_sightoing(<id>) 
The corresponding bird_sighting is deleted from the database
"""
@pytest.mark.asyncio
async def test_delete_bird_sighting(db_connection):
    await db_connection.seed('lib/db/seeds/birdfood_app.sql')
    repository = SightingRepository(db_connection)
    await repository.delete_bird_sighting(2)
    remaining_sightings = await repository.get_all_sightings()
    assert remaining_sightings == [
        Sighting(1, 'Flamingo', '2024-12-01', 'Shoreditch', None, 1),
        Sighting(3, 'Peregrine Falcon', '2024-12-01', 'Wimbledon', None, 3),
        Sighting(4, 'Resplendent Quetzal', '2024-12-01', 'Greenwich', None, 3)
    ]
