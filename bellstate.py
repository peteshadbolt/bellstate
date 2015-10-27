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

SWAP_PLAYER = {"alice":"bob", "bob":"alice"}
SWAP_COLOR = {"red":"blue", "blue":"red"}

def request_wants_json():
    """ Nicked from http://flask.pocoo.org/snippets/45/ """
    best = request.accept_mimetypes \
        .best_match(["application/json", "text/html"])
    return best == "application/json" and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes["text/html"]

def bellstate(a, b):
    p_same = math.pow(math.cos(math.pi/8), 2)
    if a=="tails" and b=="tails": p_same = 1-p_same
    x, y = ("red", "blue") if random() < 0.5  else ("red", "blue")
    return (x, x) if random() < p_same else (x, y)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<me>")
def play(me):
    redis.delete(me)
    return render_template("wait.html", me=me)

@app.route("/<me>/<coin>")
def set(me, coin):
    other_name = SWAP_PLAYER[me]

    #Decide my color
    if redis.exists(other_name):
        other = redis.hgetall(other_name)
        p_same = math.pow(math.cos(math.pi/8), 2)
        if coin == "tails" and other["coin"] == "tails": p_same = 1-p_same
        color = other["color"] if random()<p_same else SWAP_COLOR[other["color"]]
    else:
        other = {}
        color = "red" if random() < 0.5  else "blue"
        
    redis.hmset(me, {"coin": coin, "color": color})

    if request_wants_json():
        data = {me: {"coin": coin, "color":color}, other_name:other}
        return jsonify(data)
    else:
        return render_template("result.html", me=me, coin=coin, color=color)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
