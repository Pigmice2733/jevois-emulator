# JeVois Emulator

This emulator is used to write, run, and test vision tracking code for the JeVois cameras, without an actual JeVois camera. The emulator uses a laptops built-in webcam and feeds the video stream into the vision tracking as if it came from the JeVois camera.

This project has currently only been tested on Windows.

## Installation

1. Install Python 3.x. [Installation instructions here](https://www.python.org/)

2. Install numpy (`$ pip install numpy`).

3. Install OpenCV 3. If you are not on Windows, search online for instructions on how to install OpenCV 3 for Python on your platform. If you are on Windows, find the OpenCV 3.x version corresponding to your version of Python [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv) (`-cp37` is Python 3.7.x, `-cp36` is for Python 3.6.x, etc.). In your terminal, `cd` to the folder where the file downloaded, and run `$ pip install <file name>`.

4. Clone this project from GitHub (`$ git clone https://github.com/Pigmice2733/jevois-emulator.git`) into an appropriate location.

## Usage

Put your vision tracking code in a Python file (`.py`) inside this project. To test your code, run `$ python main.py --module <name of your module>`. Just like on the JeVois camera, the name of the file and the name of the vision class in the file must match.

The toggle at the top of the OpenCV video window switches between `process` and `processNoUSB` modes.
