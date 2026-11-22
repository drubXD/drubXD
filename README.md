# Dhruv Ladani · Biomedical engineering projects

I build software that helps people interact with medical images, symptom data, and wearable signals. These three projects are featured on [my portfolio](https://dhruvladani.com/#projects).

| Project | What you can do | Demo |
| --- | --- | --- |
| [Pulse · Symptom check-in](pulse/) | Describe symptoms in your own words, add health context, and review guidance on when to seek care. | [Watch Pulse](https://dhruvladani.com/pulse-demo) |
| [Cortex · MRI brain explorer](cortex/) | Rotate a 3D cortical surface, explore a highlighted region, and inspect a local scan one slice at a time. | [Watch Cortex](https://dhruvladani.com/cortex-demo) |
| [Thought to action · Muse blink controller](muse/) | Use a Muse 2 headset to turn a blink into a jump in Chrome Dinosaur. | [Watch Muse](https://www.youtube.com/watch?v=RmzZJDpHN5w) |

## Get the projects

Install [Git](https://git-scm.com/downloads), then run the following in a terminal. Start each project's instructions from the repository root.

```sh
git clone https://github.com/drubXD/drubXD.git
cd drubXD
```

## Pulse

Pulse brings symptoms, age, relevant health history, and optional location together in a four-step check-in. The results page presents possible explanations, urgency guidance, and home-care suggestions. This educational prototype sends the check-in to Groq when you request a live assessment.

Install [Node.js 22 or newer](https://nodejs.org/en/download). The server uses Node's built-in modules. To explore the form, run `node pulse/server.mjs` and open [Pulse locally](http://127.0.0.1:4174/pulse/).

**Enable live assessments**

1. Copy `pulse/.env.example` to `pulse/.env`. In PowerShell, run `Copy-Item pulse/.env.example pulse/.env`. On macOS or Linux, run `cp pulse/.env.example pulse/.env`.
2. Open the copy and set `GROQ_API_KEY=your_own_key_here` using a [Groq API key](https://console.groq.com/keys) with access to `openai/gpt-oss-120b`. Keep this file local.
3. If the server is running, press Ctrl+C. Restart it with the command below, then open [Pulse locally](http://127.0.0.1:4174/pulse/).

```sh
node --env-file=pulse/.env pulse/server.mjs
```

Web fonts, map tiles, and live assessments use internet services. Generated answers can differ from the recording.

## Cortex

Cortex pairs an interactive anatomical reference with a local image viewer. Rotate the brain to examine the highlighted region, or load a 3D NIfTI file to scroll through slices and adjust the intensity threshold. PNG, JPEG, and WebP images open in a separate 2D viewer with brightness, contrast, zoom, and PNG export. Uploaded images stay in browser memory.

Use Node.js 22 or newer and a WebGL-capable browser. The repository includes Three.js, the cortical meshes, and the fonts. You can launch directly after cloning.

```sh
cd cortex
npm start
```

Open [Cortex locally](http://127.0.0.1:4173). To try the viewer with sample data, load `cortex/tests/phantom.nii.gz`. To run the imaging tests, use `npm test` inside `cortex`. [Supported formats and viewer controls](cortex/README.md)

## Muse blink controller

The Muse 2 streams EEG samples to the computer over Lab Streaming Layer (LSL). The controller monitors blink-related changes in the delta band and sends a spacebar press to the focused game. The hardware-free replay runs with Python 3 alone and prints two blink events.

```sh
python muse/blink.py --demo
```

**Play with a headset**

1. Install Python 3 and the native liblsl runtime for your operating system. Then install the Python packages with `python -m pip install -r muse/requirements.txt`.
2. Connect the Muse 2 and start one EEG stream. Use Petal Metrics with LSL output, or run `muselsl stream` in a separate terminal.
3. Run `python muse/blink.py` and blink. Once you see “Blink!” in the terminal, press Ctrl+C.
4. Open `chrome://dino` in Chrome. Run `python muse/blink.py --keyboard`, then focus the game. Blink to jump. Ctrl+C in the terminal stops the controller.

Electrode contact and other muscle movements can affect detection. [Original illustrated build guide](https://medium.com/@dhruvl/playing-the-dinosaur-game-using-mind-control-6267dbf45528)
