from config import config
from gunicorn.app.base import BaseApplication
from routes import app
class Application(BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application
    

if __name__ == "__main__":
    options = {
        'bind': "{}:{}".format(config.configurations['server']['host'], config.configurations['server']['port']),
        'workers': 8,
    }

    Application(app, options).run()

   
        
