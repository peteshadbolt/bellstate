#!/usr/bin/python
from flask import Flask, request, jsonify, render_template, redirect
from redis import StrictRedis
import arrow
import re
import random
import time

random.seed(12345)

# Monkey patch arrow's terminology
arrow.locales.EnglishLocale.timeframes["now"] = "now"

# Boot the app
app = Flask(__name__)
app.config.from_pyfile("settings.cfg")
redis = StrictRedis(app.config["REDIS_HOST"],
                    app.config["REDIS_PORT"],
                    db=0,
                    password=app.config["REDIS_PASSWORD"])


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
    if a and b:
        return jsonify({"ready": "true", "coins": [a, b]})
    else:
        return jsonify({"ready": "false"})

if __name__ == "__main__":
    app.run(host="0.0.0.0")
