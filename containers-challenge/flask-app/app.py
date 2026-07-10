import os

from flask import Flask
from redis import Redis


app = Flask(__name__)

redis_client = Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
)


@app.route("/")
def home():
    return "<h1>Welcome to the CoderCo Containers Challenge!</h1>"


@app.route("/count")
def count():
    visit_count = redis_client.incr("visit_count")
    return f"<h1>Visit count: {visit_count}</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
