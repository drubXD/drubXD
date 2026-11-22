"""Convert a rising blink artifact into one Chrome Dinosaur jump."""
import argparse
import math
from statistics import median


class BlinkDetector:
    def __init__(self, baseline, threshold=100, cooldown=0.45):
        self.baseline = baseline
        self.threshold = threshold
        self.cooldown = cooldown
        self.armed = True
        self.last_jump = -math.inf

    def update(self, value, timestamp):
        amplitude = abs(value - self.baseline)
        if amplitude < self.threshold / 2:
            self.armed = True
        if self.armed and amplitude >= self.threshold:
            self.armed = False
            if timestamp - self.last_jump >= self.cooldown:
                self.last_jump = timestamp
                return True
        return False


def stream_samples():
    from pylsl import StreamInlet, resolve_byprop

    streams = resolve_byprop("type", "EEG", timeout=8)
    candidates = [s for s in streams if "muse" in s.name().lower()]
    if len(candidates) != 1:
        raise SystemExit("Start exactly one Muse EEG stream with muselsl stream.")
    inlet = StreamInlet(candidates[0])
    try:
        while True:
            sample, timestamp = inlet.pull_sample(timeout=3)
            if sample is None:
                raise SystemExit("Muse stream timed out. Check the connection.")
            value = (sample[1] + sample[2]) / 2  # AF7 and AF8 in MuseLSL order
            if math.isfinite(value):
                yield value, timestamp
    finally:
        inlet.close_stream()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--keyboard", action="store_true", help="Send space to focused window")
    parser.add_argument("--threshold", type=float, default=100, help="Microvolts above baseline")
    args = parser.parse_args()
    if not math.isfinite(args.threshold) or args.threshold <= 0:
        parser.error("Threshold must be finite and positive.")
    if args.demo:
        samples = ((150 if i in (200, 201, 350) else 0, i / 100) for i in range(400))
    else:
        samples = stream_samples()
    keyboard = None
    if args.keyboard:
        from pynput.keyboard import Controller, Key
        keyboard = Controller()
    print("Relax for calibration and keep the target window focused.", flush=True)
    baseline = median(next(samples)[0] for _ in range(128))
    detector = BlinkDetector(baseline, args.threshold)
    for value, timestamp in samples:
        if detector.update(value, timestamp):
            print(f"Jump at {timestamp:.2f}s", flush=True)
            if keyboard:
                keyboard.tap(Key.space)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
