from app import create_app, get_adress_and_port

# creating a flask app by calling the function
app = create_app()
address_and_port = get_adress_and_port()
address = address_and_port[0]
port = address_and_port[1]

if __name__ == "__main__":
    app.run(host=address, port=port, debug=True)