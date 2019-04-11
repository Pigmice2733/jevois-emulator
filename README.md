# JeVois Emulator

This emulator is used to write, run, and test computer vision code for the JeVois cameras, without an actual JeVois camera. The emulator uses a laptop's built-in webcam and feeds the video stream into the computer vision code as if it came from the JeVois camera.

This project has currently only been tested on Windows.

## Installation

1. Install Python 3.x. [Installation instructions here](https://www.python.org/)

2. Install numpy.

   ```
   pip install numpy
   ```

3. Install OpenCV 3. If you are not on Windows, search online for instructions on how to install OpenCV 3 for Python on your platform. If you are on Windows, find and download the OpenCV 3.x version corresponding to your version of Python [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv) (`-cp37` is Python 3.7.x, `-cp36` is for Python 3.6.x, etc.). In your terminal, navigate (using `cd`) to the folder where the file downloaded into, and use the following command to install it via pip.

   ```
   pip install <full file name>
   ```

4. Clone this project from GitHub into an appropriate location by opening a terminal, navigating to the folder you want to store the project in, and running the following command.

   ```
   git clone https://github.com/Pigmice2733/jevois-emulator.git
   ```

## Usage

Put your computer vision code in a Python (`.py`) file in a folder inside this project. To test your code, run:

```
python main.py --module <name of your module>
```

Just like on the JeVois camera, the name of the file, the folder, and the name of the vision class in the file must match.

The toggle at the top of the OpenCV video window switches between `process` and `processNoUSB` modes.

Either type `Ctrl+C` in your terminal to kill the emulator or click on the emulator window and press the escape key.

## Example

This project comes with an example module, called `Example`. This module tracks a red and a blue ball, although the masking values may need to be adjusted for it to work well depending on the lighting, and the camera used. Once the project is installed, you should be able to run the example with the command

```
python main.py --module Example
```

If this doesn't work, double check the installation steps and make sure you didn't miss any. If you still can't get it to work, open an issue asking for help, and add the label `help wanted`.

## Bugs and Feature Requests

If you come across a bug, or have a feature request, please open an issue on this GitHub project and explain the bug or the feature request.
