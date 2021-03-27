import os

from flask import Flask, request
from parse import Elec
app = Flask(__name__)


@app.route('/', methods=["POST"])
def hello_world():
    xiaoqu = request.form.get("xiaoqu")
    louming = request.form.get("louming")
    fangjian = request.form.get("fangjian")
    elec = Elec(xiaoqu, louming, fangjian)
    return elec.getElec()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
