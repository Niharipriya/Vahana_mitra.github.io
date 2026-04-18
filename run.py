from app import create_app, db, DevelopmentConfig
from flask_migrate import Migrate
import app.utils

app = create_app(config_class=DevelopmentConfig)
migrate = Migrate(app, db)

if __name__ == "__main__":
      app.run(debug=True)