import sys, os
from flask import Flask, render_template, jsonify
from flask_cors import CORS, cross_origin
import sys
import housing
from housing.logger import logging
from housing.exception_handler import HousingException


app = Flask(__name__)
CORS(app)


@app.route("/", methods=['POST', 'GET'])
@cross_origin()
def index():

    try: 
        raise Exception("We are testing custom excecption")
        # print(3/0)
    except Exception as e:
        housing = HousingException(e, sys)
        logging.info(housing.error_message)

    logging.info("We are testing logging module")
    return "CI/CD Pipeline for our Project has been established"


if __name__ == '__main__':

    app.run(debug=True)


