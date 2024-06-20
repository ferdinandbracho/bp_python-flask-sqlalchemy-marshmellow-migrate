from marshmallow import EXCLUDE, fields

from app import config
from app.models.stations_models import Station

# Setting database and marshmallow
db = config.db


# Base station schema
class StationSchema(config.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Station
        load_instance = True
        sqla_session = db.session
    geojson = fields.Dict()
    address = fields.String(allow_none=True, default='--')


station_schema = StationSchema()
stations_schema = StationSchema(many=True)


# Compact station schema
class PropertiesSchema(config.ma.Schema):
    class Meta:
        unknown = EXCLUDE
    name = fields.String(default=None, allow_none=True)
    address = fields.String(default=None, allow_none=True)


class GeojsonSchema(config.ma.Schema):
    class Meta:
        unknown = EXCLUDE
    properties = fields.Nested(PropertiesSchema)


class CompactStationSchema(config.ma.Schema):
    client_id = fields.Raw(required=True)
    latitude = fields.Raw(required=True)
    longitude = fields.Raw(required=True)
    geojson = fields.Nested(GeojsonSchema, required=True)


compact_station_schema = CompactStationSchema()


# Update Station
class UpdateStationSchema(config.ma.Schema):
    name = fields.String(allow_none=True)
    geofence_radius = fields.Integer(allow_none=True)
    address = fields.String(allow_none=True)
    latitude = fields.String(allow_none=True)
    longitude = fields.String(allow_none=True)
    description = fields.String(allow_none=True)
    active = fields.Bool(allow_none=True)


update_station_schema = UpdateStationSchema()
