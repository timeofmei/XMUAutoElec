import ujson
import httpx
from flask import Flask, request
from parse import Elec
app = Flask(__name__)


@app.route('/', methods=["POST"])
def hello_world():
    data = request.get_data()
    json_data = ujson.loads(data.decode("utf-8"))
    xiaoqu = json_data.get("xiaoqu")
    louming = json_data.get("louming")
    fangjian = json_data.get("fangjian")
    elec = Elec(xiaoqu, louming, fangjian)
    result = ujson.dumps(elec.getElec(), ensure_ascii=False)
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
