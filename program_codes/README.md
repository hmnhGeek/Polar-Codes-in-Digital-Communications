# Polar Codes: Practical Encoding and Decoding Algorithms
This project deals with the study of polar codes in detail. While the study was going on, various other codes like repitition codes and hamming codes were also considered in the study. So the repository contains the related codes as well.

## Hamming Code (7, 4) Bit Error Rate Simulator
```
idle3 hammingcode74.py
```
The above line opens the ```.py``` file in the IDLE. From there you can run ```plot()``` function. Please read the code to understand about the functions.

## Polar Code BER Simulation and Encoder-Decoder Pair
```
idle3 polar_encoding.py
```
Open the above ```.py``` file using IDLE. Using ```encode()``` function, a random message is shown encoded using polar encoding scheme. Currently, this ```.py``` file only supports polar encoding at N = 16. The current 5G standard uses N=1024. Full documentation of the encode function is written in the document. Similarly, to decode a given a polar code using ```decode()``` function. From the ```.py``` file you can run ```simulate1()``` or ```simulate2()``` function. Documentation for both these functions is given in the code.

You can also try the Monte Carlo simulation by using ```monte_carlo()``` function.

## Matthew Effect and Reliability Sequence
If you run ```python3 matthew_effect.py```, a matplotlib window will pop up which will show that as more copies of a given B-DMC are used for channel polarization, the capacities of the good channels approach 1.

If you issue ```idle3 reliability_seq_gen.py``` in the terminal, the ```.py``` file will open and from there you can use the functions ```matthew_effect_good()``` and ```matthew_effect_bad()``` which will generate matplotlib windows showing the variations in the **good** and **bad** channel capacities vs. transitions probabilities of the B-DMC. Also, use ```polarize()``` function to generate all the channel capacities for the N level polarized channels. Use, ```reliability_sequence()``` function to generate a reliability sequence for any N and a given BEC transition probability.

## AWGN Web App
This is a simple web app which simulates the effect of AWGN on a given message bit stream. It requires ```textwrap3``` module. Please install via ```pip3``` before using this app. After installation of textwrap, issue ```python3 app.py``` and then head on to a browser at the following URL ```127.0.0.1:5000/```. That's it, follow the steps now.
