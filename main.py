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
    try:
        result = ujson.dumps(elec.getElec(), ensure_ascii=False)
    except httpx.ConnectTimeout:
        return ujson.dumps({"账户余额": -2.0, "剩余电量": -2.0})
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
