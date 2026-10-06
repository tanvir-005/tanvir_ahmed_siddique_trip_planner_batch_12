from flask import Flask 

# function to create Flask app
def create_app():
    app = Flask(__name__)
    return app