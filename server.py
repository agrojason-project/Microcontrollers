#!/usr/bin/env python3
from flask import Flask, render_template, redirect, request, make_response, url_for
from codex.en_de import *
import socket

app = Flask(__name__)


Host = '192.168.2.2'
Port = 12345
msg_resv = ''

def send(message: str):
    s = socket.socket()
    s.connect((Host,Port))
    message = my_encode(message)
    s.send(message)
    msg = s.recv(1024)
    s.close()
    msg = my_decode(msg)
    return msg
    return 

@app.route("/options",methods = ['GET', 'POST'])
def options():
    global msg_resv
    if request.method == 'POST':
        if request.form['option'] != "":
            make_response(render_template('options.html'))
            msg_send  = request.form['option']
            msg_resv = send(msg_send)
            return redirect(url_for('result'))
    return render_template('options.html')

@app.route("/result",methods = ['GET', 'POST'])
def result():
    global msg_resv
    print(msg_resv)
    if request.method == 'POST':
        return redirect(url_for('options'))
    return render_template('result.html', message = msg_resv)

    
app.debug = True
app.run(host="0.0.0.0", port=8008)