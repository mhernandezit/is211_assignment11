from app import create_app
import os
import app.models

application = create_app(os.getenv('FLASK_CONFIG') or 'default')


if __name__ == "__main__":
    application.run()