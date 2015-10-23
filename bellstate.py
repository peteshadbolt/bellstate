#!/usr/bin/python
from flask import Flask, request, jsonify, render_template, redirect
from redis import StrictRedis
import math
from random import random

# Boot the app
app = Flask(__name__)
app.config.from_pyfile("settings.cfg")
redis = StrictRedis(app.config["REDIS_HOST"],
                    app.config["REDIS_PORT"],
                    db=0,
                    password=app.config["REDIS_PASSWORD"])


def bellstate(a, b):
    p_same = math.pow(math.cos(math.pi/8), 2)
    if a=="tails" and b=="tails": p_same = 1-p_same
    x, y = ("red", "blue") if random() < 0.5  else ("red", "blue")
    return (x, x) if random() < p_same else (x, y)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<me>")
def get(me):
    state = str(redis.get(me))
    return jsonify({"who": me, "state": state})


@app.route("/<me>/<my_coin>")
def set(me, my_coin):
    redis.set(me, my_coin)
    msg = "Set {}'s coin to {}".format(me, my_coin)
    return jsonify({"message": msg})


@app.route("/reset")
def reset():
    redis.set("alice", None)
    redis.set("bob", None)
    msg = "Reset the game"
    return jsonify({"message": msg})


@app.route("/poll")
def poll():
    a = redis.get("alice")
    b = redis.get("bob")
    if a!="None" and b!="None":
        output = bellstate(a, b)
        output = {"alice": output[0], "bob":output[1]}
        return jsonify({"ready": "true", "coins": [a, b], "output": output})
    else:
        return jsonify({"ready": "false"})

if __name__ == "__main__":
    app.run(host="0.0.0.0")
