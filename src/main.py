"""
This is the main entry point for the Flask application.

It creates the Flask app and runs it on the default port.
"""
from app import create_app


if __name__ == "__main__":
    # Create the Flask app and run it on the default port
    # The app is created using the create_app function from the app module
    app = create_app()
    app.run()
