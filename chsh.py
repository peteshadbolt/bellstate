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
def player(me):
    return render_template("player.html", me=me)

@app.route("/<me>/<my_coin>")
def output(me, my_coin):
    redis.set(me, my_coin)
    other = {"alice":"bob", "bob":"alice"}[me]
    other_coin = redis.get(other)
    if other_coin == None:
        return render_template("waiting.html", me=me, my_coin=my_coin, other=other)
    else:
        redis.delete(other)
        output = str(random.randint(0,100))
        return render_template("output.html", me=me, other=other, my_coin=my_coin, other_coin=other_coin, output=output)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
