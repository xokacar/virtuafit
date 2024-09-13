from flask import Flask
from routes import auth_blueprint
from models import Base
from database import engine
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


Base.metadata.create_all(bind=engine)


app.register_blueprint(auth_blueprint)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')