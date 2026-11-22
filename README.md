# Dhruv Ladani · Biomedical engineering projects

Three projects explore how software can make medical images, symptom data, and wearable signals easier to interact with. These portfolio editions reconstruct earlier projects from development conversations. The original laptop folders, disease database, and trained model weights were unavailable.

| Project | Try it locally from the repository root |
| --- | --- |
| [Muse blink controller](muse/) | `python muse/blink.py --demo` prints two jump events from a simulated stream. |
| [MRI Reader](mri-reader/) | Install its requirements and run `python mri-reader/viewer.py`. Open the printed HTML path and scroll through a synthetic volume. |
| [HealthGuard](healthguard/) | `python healthguard/app.py sneezing "itchy eyes"` ranks entries from a small, editable teaching catalog. |

### Muse blink controller

The 2023 prototype used MuseLSL, threshold detection, and a spacebar press to control Chrome Dinosaur. This version rebuilds the incomplete acquisition loop using an LSL inlet, frontal-channel averaging, baseline calibration, rearming, and a cooldown. Watch the [original project demo](https://youtu.be/RmzZJDpHN5w).

For live mode, install `pip install -r muse/requirements.txt` and the native liblsl runtime for your OS. Pair the headset and run `muselsl stream` in one terminal. In another run `python muse/blink.py` to observe events. Use `--keyboard` to enable spacebar presses and focus the game. Adjust `--threshold` in microvolts for your signal. Motion and poor electrode contact can also trigger the detector.

### MRI Reader

Install `pip install -r mri-reader/requirements.txt`. Supply a 3D NIfTI, a grayscale DICOM file (single or multiframe), or a PNG/JPEG to `python mri-reader/viewer.py INPUT --out scan.html`. The exported viewer embeds the image pixels. Keep exports containing private images local. DICOM series assembly and diagnostic measurement are outside this edition.

For optional segmentation install `pip install torch monai` and run `python mri-reader/segment.py volume.nii.gz model.pt mask.nii.gz`. Supply a trusted TorchScript model trained for single-channel, RAS-oriented, native-spacing volumes with nonzero-voxel z-score normalization, 96³ patches, and one binary logit per voxel. Verify that acquisition modality and spacing match the model training data. Model weights are a separate dependency from the optional text API.

### HealthGuard

Run without arguments to list the supported symptom terms. The score divides shared terms by the union of selected and catalog terms. Up to three matches show exactly which terms contributed. Use `--catalog PATH` with a JSON object mapping condition names to lowercase symptom lists to substitute a larger catalog. The five included sample entries illustrate ranking mechanics. This edition has no measured clinical accuracy.

### Optional AI explanations

Both health projects run their local demos without credentials. To explain catalog results or simplify an existing report, copy `.env.example` to `.env` and supply your own Anthropic API key and enabled model ID. For example, in Bash, load the settings and generate a match file:

```sh
python healthguard/app.py sneezing "itchy eyes" > matches.txt
set -a
source .env
set +a
```

Then run `python explain.py healthguard matches.txt` or `python explain.py mri-reader report.txt`. The explanation command sends that text to Anthropic and may incur charges. Use synthetic or de-identified text. These are educational research prototypes.
