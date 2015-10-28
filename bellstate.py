#!/usr/bin/python
from flask import Flask, request, jsonify, render_template, redirect
from redis import StrictRedis
import math
from random import random
from shortuuid import ShortUUID

# Boot the app
app = Flask(__name__)
app.config.from_pyfile("settings.cfg")
redis = StrictRedis(app.config["REDIS_HOST"],
                    app.config["REDIS_PORT"],
                    db=0,
                    password=app.config["REDIS_PASSWORD"])

SWAP_PLAYER = {"alice":"bob", "bob":"alice"}
SWAP_COLOR = {"red":"blue", "blue":"red"}
UUID_TIMEOUT = 60

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
    if redis.exists("uuid"):
        uuid = redis.get("uuid")
        redis.delete("uuid")
    else:
        uuid = ShortUUID().random(length=10)
        redis.set("uuid", uuid)
        redis.set(uuid+":score", 0)
        redis.set(uuid+":attempts", 0)
        redis.expire("uuid", UUID_TIMEOUT)
    return render_template("index.html", uuid=uuid)

@app.route("/<uuid>/<me>")
def play(uuid, me):
    redis.delete(uuid+":"+me)
    return render_template("wait.html", me=me, uuid=uuid)

@app.route("/<uuid>/<me>/<coin>")
def set(uuid, me, coin):
    other_name = SWAP_PLAYER[me]

    #Decide my color
    if redis.exists(uuid+":"+other_name):
        other = redis.hgetall(uuid+":"+other_name)
        p_same = math.pow(math.cos(math.pi/8), 2)
        if coin == "tails" and other["coin"] == "tails": p_same = 1-p_same
        color = other["color"] if random()<p_same else SWAP_COLOR[other["color"]]

        redis.incr(uuid+":attempts")    
        if coin=="heads" or other["coin"]=="heads" and color == other["color"]:
            redis.incr(uuid+":score")    
        if coin=="tails" and other["coin"]=="tails" and color != other["color"]:
            redis.incr(uuid+":score")    
    else:
        other = {}
        color = "red" if random() < 0.5  else "blue"

    score = redis.get(uuid+":score")
    attempts = redis.get(uuid+":attempts")

    redis.hmset(uuid+":"+me, {"coin": coin, "color": color})

    if request_wants_json():
        data = {me: {"coin": coin, "color":color}, other_name:other}
        return jsonify(data)
    else:
        return render_template("result.html", me=me, coin=coin, color=color, uuid=uuid, score=score, attempts=attempts)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
