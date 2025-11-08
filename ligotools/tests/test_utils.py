import numpy as np
from ligotools.utils import whiten, reqshift

def test_whiten_basic_properties():
    strain = np.random.normal(0, 1, 4096)
    freqs = np.fft.rfftfreq(len(strain), 1/4096)

    psd = np.ones_like(freqs) * 2.0
    interp_psd = lambda f: np.ones_like(f) * 2.0
    dt = 1/4096

    white = whiten(strain, interp_psd, dt)

    assert np.isrealobj(white), "Whitened output should be real-valued"
    assert len(white) == len(strain), "Whitened signal must preserve length"
    assert abs(np.mean(white)) < 1, "Whitened signal should be zero-mean"
    assert np.any(white != 0), "Whitened signal should not be all zeros"
    assert not np.isnan(white).any(), "Whitened signal should not contain NaNs"


def test_reqshift_frequency_shift():
    fs = 4096
    t = np.linspace(0, 1, fs)
    f0 = 100  # base frequency
    fshift = 50  # shift frequency
    sig = np.sin(2 * np.pi * f0 * t)

    shifted = reqshift(sig, fshift = fshift, sample_rate = fs)

    # Check signal properties
    assert np.isrealobj(shifted), "Shifted signal should be real-valued"
    assert len(shifted) == len(sig), "Shifted signal length mismatch"
