# Thought to action · Muse 2
The game interface is Chrome Dinosaur itself. A blink-related change in the EEG stream sends Space to the focused game. This controller reconstructs the signal path in [Dhruv’s build guide](https://medium.com/@dhruvl/playing-the-dinosaur-game-using-mind-control-6267dbf45528). [Watch the original demonstration](https://www.youtube.com/watch?v=RmzZJDpHN5w).

1. Run `python blink.py --demo` to replay two events without hardware.
2. For hardware, install the native liblsl runtime for your OS and run `python -m pip install -r requirements.txt`. Connect a Muse 2 using Petal Metrics with LSL output, or start a compatible EEG stream with `muselsl stream`.
3. Run `python blink.py` and blink. Check for a printed event. To inspect the signal separately, use `muselsl view` with its viewer dependencies installed.
4. Open `chrome://dino` in Chrome. Run `python blink.py --keyboard` and focus the game. Grant your terminal accessibility permission if your OS requires it. Ctrl+C stops the controller.

The tutorial uses the first channel, a one-second analysis window, and delta-band thresholds of 1 and 1.7 on the MuseLSL log scale. Contact quality and other muscle movements can affect the result. The bundled signal_utils.py comes from the MuseLSL example utilities and retains its upstream license alongside it.
