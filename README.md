# Dhruv Ladani
Biomedical engineering, medical imaging, and neurotechnology. These are the projects featured on [my portfolio](https://dhruvladani.com/#projects).

| Project | Run it from a fresh clone | Original demonstration |
| --- | --- | --- |
| [Pulse · Symptom check-in](pulse/) | With Node.js 22+, run `node pulse/server.mjs` and open **http://127.0.0.1:4174/pulse/**. | [Watch Pulse](https://dhruvladani.com/pulse-demo) |
| [Cortex · Brain explorer](cortex/) | With Node.js 22+, run `cd cortex`, then `npm start`. Open **http://127.0.0.1:4173** in a WebGL-capable browser. | [Watch Cortex](https://dhruvladani.com/cortex-demo) |
| [Thought to action · Muse 2](muse/) | Run `python muse/blink.py --demo` for a hardware-free replay. Follow the project instructions for live blink control in Chrome Dinosaur. | [Watch Muse](https://www.youtube.com/watch?v=RmzZJDpHN5w) |

**Pulse** includes the portfolio implementation of the four-step check-in, optional map and assessment results. To enable live assessments, copy `pulse/.env.example` to `pulse/.env`, enter your own Groq API key, then start with `node --env-file=pulse/.env pulse/server.mjs`. The map, web fonts and live assessments use external services. The form opens without a key. Live answers can differ from the recorded example.

**Cortex** ships the original interface, 3D cortical meshes, viewer controls, fonts, published case illustration, local imaging tools and tests. It runs locally without an API key. Run `npm test` inside the cortex folder.

**Muse** uses the published tutorial’s thresholds and the Chrome Dinosaur game. Live testing requires a compatible headset and an LSL stream.
