from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_pyfile('config.py')
csrf = CSRFProtect(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from views import *

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if __name__ == '__main__':
    app.run(debug=True)
