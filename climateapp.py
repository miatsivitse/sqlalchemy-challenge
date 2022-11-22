    from flask import Flask

    app = Flask(__name__)

    @app.route("/api/v1.0/precipitation")
    def precip():
        print("Server received request for 'Home' page...")
        return "Welcome to my 'Home' page!"

    @app.route("/api/v1.0/stations")
    def stations():
        print("Server received request for 'Home' page...")
        return "Welcome to my 'Home' page!"

    @app.route("/api/v1.0/tobs")
    def tobs():
        print("Server received request for 'Home' page...")
        return "Welcome to my 'Home' page!"

    @app.route("/api/v1.0/<start>")
    def tobs():
        print("Server received request for 'Home' page...")
        return "Welcome to my 'Home' page!"

    @app.route("/api/v1.0/<start>/<end>")
    def tobs():
        print("Server received request for 'Home' page...")
        return "Welcome to my 'Home' page!"

    if __name__ == "__main__":
        app.run(debug=True)