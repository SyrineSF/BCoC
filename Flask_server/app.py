#!/usr/bin/python3
from flask import Flask
from Bleuprints.auth import auth_bp
from Bleuprints.general import general
from Bleuprints.first_responder import first_responder
from Bleuprints.investigator import investigator
from Bleuprints.lawyer import lawyer


app = Flask(__name__)
app.secret_key = 'secret_key'
app.register_blueprint(auth_bp)
app.register_blueprint(general)

app.register_blueprint(first_responder)
app.register_blueprint(investigator)
app.register_blueprint(lawyer)



if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)