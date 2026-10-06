from app import create_app

# creating a flask app by calling the function from
app = create_app()

# /health route to get json and 200 status code
@app.route("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(debug=True)