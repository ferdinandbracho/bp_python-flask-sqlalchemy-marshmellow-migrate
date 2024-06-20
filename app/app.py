from flask import redirect
from flask_cors import CORS
from flask_migrate import Migrate

from app import config

# Init API
config.connex_app.add_api(f'{config.basedir.parent}/swagger.yml')
app = config.connex_app.app

# Cors
CORS(app)

# Migration
migrate = Migrate(app, config.db)


@app.route('/docs')
def docs():
    return redirect('/api/dev/ui')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)
