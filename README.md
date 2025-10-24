# basic_image_detection_program
a python program that allows the user to click and drag to select a portion of their screen to try to detect what the user has selected. using pytorch/torchvision

This program was mostly just to get me back into Python programming after focusing on other languages so it is quite basic. 

the exe file was too large for Github so you'll have to make sure you have Python 3.8+ installed. Then install the required packages:
pip install torch torchvision pillow requests

Save the code in a file named image_detection.py (or any name you prefer), then run: 
python image_detection.py

or you could use pyinstaller to convert it into an exe file for windows

to use the program, just click and drag a section of yout window (like windows snipping tool) and the program will give you its best guess. From there your only two options are to make another selection and to exit the program.
