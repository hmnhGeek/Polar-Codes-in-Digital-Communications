from flask import Flask, render_template, request, url_for
from White_Gaussian import awgn_simulator
import numpy as np
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/simulator_results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        ebno = request.form['ebno']
        R = request.form['rate']
        message = request.form['msg']

        ebno = float(ebno)
        R = float(R)

        results = awgn_simulator.init_simulator(ebno, R, message)
        string_result = "BER = {} <br><br> Received Message = {} <br><br> Theoretical BER = {} <br><br> Sent Message = {}".format(results[0], results[1], results[2], message)

        if R == 1.0:
            string_result = "<h2> Uncoded Modulation </h2>" + string_result

        if results[0] != 0.0:
            string_result += "<br><br><br> Increase energy per bit to remove the effect of white noise."
        else:
            string_result += "<br><br><br> There were no errors in the transmission."

        return render_template('results.html', noise=url_for('static', filename='noise.png'), string=string_result)

@app.route('/form2')
def form2():
    return render_template('form2.html')

@app.route('/optimal_bit_energy', methods=['GET', 'POST'])
def optimal():
    if request.method == 'POST':
        R = request.form['rate']
        message = request.form['message']
        R = float(R)

        ebono = 1.0
        while awgn_simulator.init_simulator(ebono, R, message)[0] != 0.0:
            ebono += 0.1

        return str(ebono)
        
if __name__ == '__main__':
    app.run(debug=True)
    
