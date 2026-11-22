"""Play Chrome Dinosaur using the blink rule from Dhruv's Muse 2 guide."""
import argparse


def playback(levels, press):
    previous = 0.0
    for current in levels:
        onset = current >= 1 and previous <= 1
        quick_blink = current >= 1.7 and previous >= 1
        if onset or quick_blink:
            print("Blink!", flush=True)
            press()
        previous = current


def delta_levels():
    import numpy as np
    from pylsl import StreamInlet, resolve_byprop
    from signal_utils import update_buffer, compute_band_powers

    streams = resolve_byprop('type', 'EEG', timeout=8)
    if len(streams) != 1:
        raise SystemExit('Start exactly one EEG stream in Petal Metrics or MuseLSL.')
    inlet = StreamInlet(streams[0])
    try:
        rate = int(round(inlet.info().nominal_srate()))
        if rate < 8:
            raise SystemExit('Expected a regularly sampled Muse EEG stream.')
        buffer = np.zeros((rate, 1))
        state = None
        while True:
            chunk, _ = inlet.pull_chunk(timeout=1, max_samples=max(1, int(0.2 * rate)))
            if not chunk:
                continue
            channel = np.asarray(chunk)[:, :1]
            buffer, state = update_buffer(buffer, channel, notch=True, filter_state=state)
            yield float(compute_band_powers(buffer, rate)[0])
    finally:
        inlet.close_stream()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--demo', action='store_true', help='Replay two synthetic blink events')
    parser.add_argument('--keyboard', action='store_true', help='Send Space to the focused game')
    args = parser.parse_args()
    def press_space():
        if args.keyboard:
            import pyautogui
            pyautogui.press('space')
    try:
        playback([0.2, 1.2, 1.3, 1.75, 0.4] if args.demo else delta_levels(), press_space)
    except KeyboardInterrupt:
        pass
