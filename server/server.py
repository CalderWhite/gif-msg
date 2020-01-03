#!/usr/bin/python3
"""
WARNING:
This is a very simple server that I threw together so I could use gif_msg on the web.
Carefully think about your environment and the security of this application before using it.
"""
from flask import Flask, request, send_file
from PIL import Image
import logging

import gif_msg

app = Flask(__name__)


@app.route("/api/encode", methods=['POST'])
def encode_endpoint():
    if 'file' not in request.files:
        return "Missing file in form.", 400
    im = Image.open(request.files['file'].stream)

    plaintext = request.form.get('plaintext', '')
    if plaintext == '':
        return "Missing plaintext in form.", 400

    bytes_out = gif_msg.encode_gif(im, plaintext)
    return send_file(
        bytes_out,
        mimetype='image/gif'
    )


@app.route("/api/decode", methods=['POST'])
def decode_endpoint():
    if 'file' not in request.files:
        return "Missing file in form.", 400
    im = Image.open(request.files['file'].stream)

    plaintext = gif_msg.decode_gif(im)

    return plaintext


@app.route("/")
def index():
    return send_file("index.html")


def run():
    app.run()


def run_prod():
    app.run(host="0.0.0.0", port=80)


if __name__ == '__main__':
    run()
