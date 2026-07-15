import os
import socket

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
    container_name = socket.gethostname()

    return f"""
    <h1>Visit Count: {visit_count}</h1>
    <p>Handled by Flask container: {container_name}</p>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
