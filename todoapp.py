from app import create_app
import os


application = create_app(os.getenv('FLASK_CONFIG') or 'default')


if __name__ == "__main__":
    application.run()
