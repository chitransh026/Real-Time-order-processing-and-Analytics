from flask import Flask
from flask import request
from flask import jsonify

from producer import send_order

app = Flask(__name__)

@app.route("/")
def home():

    return {
        "service": "Producer Service"
    }

@app.route("/order", methods=["POST"])
def create_order():

    order = request.json

    send_order(order)

    return jsonify(
        {
            "message": "Order Sent",
            "order": order
        }
    )

if __name__ == "__main__":
    app.run(debug=True)