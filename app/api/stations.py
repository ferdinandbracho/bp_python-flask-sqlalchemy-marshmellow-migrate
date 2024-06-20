from marshmallow import ValidationError

from app import config
from app.models.stations_models import Station
from app.schemas.station_schema import (
    StationSchema,
    UpdateStationSchema,
    station_schema,
    stations_schema
)
from app.utils import get_address

# Setting necessary interfaces
db = config.db
logger = config.logger


# Create
def create_station(station: StationSchema) -> tuple:
    res: dict = {}

    # Validating provided data
    try:
        # Validate address and name to create in case of need
        lat, lon = station['latitude'], station['longitude']
        name = station['name'] if 'name' in station else f'{lat}-{lon}'
        station.update({'name': name})

        if 'address' not in station:
            station.update({'address': get_address(lat, lon)})
        new_station = station_schema.load(station)
    except ValidationError as e:
        res.update({'validation_failed': e.messages})
        logger.exception(msg=e.messages)
        return res, 400
    try:
        # Searching for existing station with same location in client scope
        existing_station = Station.query.filter(
            Station.client_id == station['client_id'],
            Station.longitude == station['longitude'],
            Station.latitude == station['latitude']
            ).first()

        # Returning error
        if existing_station:
            res.update({'station_already_exist': {
                'name': existing_station.name,
                'id': existing_station.id
                }
            })
            logger.error(msg=res, exc_info=True)
            return res, 400

        # Creating new station
        else:
            db.session.add(new_station)
            db.session.commit()
            return station_schema.dump(new_station), 201

    # Cath and return unexpected exception
    except Exception as e:
        res.update({'exception': str(e)})
        logger.exception(msg=str(e))
        return res, 400


# Details
def retrieve_station(station_id: int) -> tuple:
    res = {}
    try:
        # Searching for existing station with same location in client scope
        existing_station = Station.query.get(station_id)

        # Returning station
        if existing_station:
            return station_schema.dump(existing_station), 200
        else:
            res.update({'failed': 'Station not found'})
            return res, 404

    # Cath and return unexpected exception
    except Exception as e:
        res.update({'exception': str(e)})
        logger.exception(msg=str(e))
        return res, 400


# List
def list_stations(
        client_id: int,
        page: int,
        limit: int = 50) -> tuple:
    res: dict = {}
    try:
        # Searching for stations in indicated client scope
        existing_stations = Station.query.filter(
            Station.client_id == client_id).paginate(
            page=page,
            per_page=limit,
            error_out=False
        )

        # Returning station list
        return stations_schema.dump(existing_stations), 200

    # Cath and return unexpected exception
    except Exception as e:
        res.update({'exception': str(e)})
        logger.exception(msg=str(e))
        return res, 400


# Update
def update_station(
    station_id: int,
    data_to_update: UpdateStationSchema
) -> tuple:
    res: dict = {}
    # Searching for existing station
    existing_station = Station.query.get(station_id)

    # updating
    if existing_station:
        for field in data_to_update:
            if field in existing_station.__dict__:
                setattr(existing_station, field, data_to_update[field])

        db.session.merge(existing_station)
        db.session.commit()

        return station_schema.dump(existing_station), 200
    else:
        res.update({'failed': 'Station not found'})
        return res, 404


# Delete
def delete_station(station_id: int):
    res: dict = {}
    # Searching for existing station
    existing_station = Station.query.get(station_id)

    # Deleting
    if existing_station:
        db.session.delete(existing_station)
        db.session.commit()
        res.update({'is_delete': True})
        return res, 200
    else:
        res.update({'failed': 'Station not found'})
        return res, 404
