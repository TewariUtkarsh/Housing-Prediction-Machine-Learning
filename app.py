from flask import Flask, render_template, jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)


@app.route("/", methods=['POST', 'GET'])
@cross_origin()
def index():
    return "Starting Machine Learning Project"


if __name__ == '__main__':

    app.run(debug=True)