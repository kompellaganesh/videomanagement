from flask import Flask
from config.config import  configurations
from routes.uploadvideo_handler import uploadvideo
from flasgger import Swagger
from routes.listvideo_handler import listvideos
from routes.streamvideo_handler import streamvideo
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

app.add_url_rule(configurations['server']['apipath']+"/api/v1/uploadvideo","uploadvideo",uploadvideo,methods=['POST'])  
app.add_url_rule(configurations['server']['apipath']+"/api/v1/listvideos","listvideos",listvideos)  
app.add_url_rule(configurations['server']['apipath']+"/api/v1/streamvideo","streamvideo",streamvideo)  
swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True, 
            "model_filter": lambda tag: True, 
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/v1/swagger",
    "url_prefix": configurations['server']['apipath']
}
app.config['SWAGGER'] = {
    'openapi': '3.0.2',
    'title':"Videos Service"
}
swagger = Swagger(app, config=swagger_config)
