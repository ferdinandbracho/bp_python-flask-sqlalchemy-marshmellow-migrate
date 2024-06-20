import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID

from app import config


# date function
def _get_date():
    return datetime.datetime.now(datetime.timezone.utc)


# Setting database and marshmallow
db = config.db


class Station(config.db.Model):
    __tablename__ = 'station'
    id = db.Column(UUID(
        as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    client_id = db.Column(db.Integer, index=True)

    name = db.Column(db.String, nullable=False,  index=True)

    geofence_radius = db.Column(
        db.Integer,
        nullable=False,
        default=10,
        index=True
    )

    address = db.Column(db.String, nullable=False)

    longitude = db.Column(db.String, nullable=False)

    latitude = db.Column(db.String, nullable=False)

    description = db.Column(db.String)

    active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.TIMESTAMP, default=_get_date)

    last_update = db.Column(
        db.TIMESTAMP,
        default=_get_date,
        onupdate=_get_date
    )
