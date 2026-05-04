import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from monitoring import detect_drift


def test_no_drift_when_close_to_baseline():
    baseline = {"mean": 100.0, "std": 20.0}
    result = detect_drift([95, 100, 105, 102, 98], baseline)
    assert result["drift"] is False


def test_drift_when_far_from_baseline():
    baseline = {"mean": 100.0, "std": 20.0}
    result = detect_drift([300, 320, 310, 305, 315], baseline)
    assert result["drift"] is True


def test_empty_input_returns_no_drift():
    baseline = {"mean": 100.0, "std": 20.0}
    result = detect_drift([], baseline)
    assert result["drift"] is False
