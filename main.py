import os
from flask import Flask
from flask_restful import Api
from application.config import LocalDevelopmentConfig
from application.database import db


app = None
api = None
def create_app():
    
    app = Flask(__name__)
    if os.getenv("ENV","development") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    return app, api

app, api = create_app()



from application.login_controllers import *
from application.profile import *
from application.post_controllers import *
from application.follow import *
from application.user_api import UserAPI
from application.post_api import PostAPI

api.add_resource(UserAPI,"/api/profile/<user_name>", "/api/profile")
api.add_resource(PostAPI,"/api/post/<user_name>", "/api/<user_name>/post/<post_id>")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8080)