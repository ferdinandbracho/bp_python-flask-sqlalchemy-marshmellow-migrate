import logging
import os
import pathlib

import connexion
from dotenv import load_dotenv
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

# Config env variable
load_dotenv()
env_path = pathlib.Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

# Setting connexion app
basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

# Setting flask app
app = connex_app.app

# Data Base
database_url = (
        f'postgresql://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}'
        f'@{os.getenv("DATABASE")}'
    )

app.config['SQLALCHEMY_DATABASE_URI'] = database_url

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db and marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Config logger
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    )

logger = logging.getLogger()
