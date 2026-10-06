from flask import Blueprint

# Blueprint initialization
blueprint = Blueprint("main", __name__)

# /health route to get json and 200 status code
@blueprint.get("/health")
def health():
    return {"status": "ok"}, 200