import numpy as np
from scipy.io.wavfile import read, write
from scipy import signal


# TODO: Replace the code below with your implementation of the waveforms.
# Hint: You may want to write more helper functions to create the waveforms
# Note: How will you handle aliasing?
def gen_wave(type, freq, dur, fs=44100, amp=1, phi=0):
    """
    Args:
    type (str) = waveform type: 'sine', 'square', 'saw', or 'triangle'
    freq (float) = fundamental frequency in Hz
    dur (float) = duration of the sinusoid (in seconds)
    fs (float) = sampling frequency of the sinusoid in Hz
    amp (float) = amplitude of the fundamental
    phi (float) = initial phase of the wave in radians
    Returns:
    The function should return a numpy array
    wave (numpy array) = The generated waveform
    """
  
    wave = np.array([])

    if type == 'sine':
        # create sinusoid
        wave = amp * np.sin(2*np.pi*freq*np.arange(0,dur,1/fs) + phi)
    elif type == 'saw':
        # create saw
        wave = np.array([])
    elif type == 'square':
        # create square
        wave = np.array([])
    elif type == 'triangle':
        # create triangle
        wave = np.array([])
    return wave
    

# TODO: Replace the code below with your implementation of an ADSR
# Hint: If you use %'s for your ADSR lengths, what length should the sustain value be
# Note: How will you handle percentages that are too long? For example, attack is 50, decay is 50, release is 50?
def adsr(data, attack, decay, sustain, release, fs=44100):
    x = np.array(data, dtype=float)
    n = x.size
    if n == 0:
        return x

    # convert to floats safely
    try: 
        A = float(attack)
    except:
        A = 0.0
    try:
        D = float(decay)
    except:
        D = 0.0
    try:
        R = float(release)
    except:
        R = 0.0
    try:
        S = float(sustain)
    except:
        S = 0.8

    # keep sustain between 0–1
    if S < 0: S = 0.0
    if S > 1: S = 1.0

    # scale A + D + R if they exceed 100%
    total = A + D + R
    if total > 100 and total > 0:
        scale = 100.0 / total
        A *= scale
        D *= scale
        R *= scale

    # convert percentages to sample lengths
    A_n = int((A / 100) * n)
    D_n = int((D / 100) * n)
    R_n = int((R / 100) * n)
    S_n = n - (A_n + D_n + R_n)

    if S_n < 0:
        S_n = 0

    # create envelope segments
    if A_n > 0:
        segA = np.linspace(0, 1, A_n, endpoint=False)
    else:
        segA = np.array([])

    if D_n > 0:
        segD = np.linspace(1, S, D_n, endpoint=False)
    else:
        segD = np.array([])

    if S_n > 0:
        segS = np.full(S_n, S)
    else:
        segS = np.array([])

    # release starts at end of sustain or decay or attack
    if S_n > 0:
        start = S
    elif D_n > 0:
        start = segD[-1]
    elif A_n > 0:
        start = segA[-1]
    else:
        start = S

    if R_n > 0:
        segR = np.linspace(start, 0, R_n)
    else:
        segR = np.array([])

    env = np.concatenate([segA, segD, segS, segR])

    # fix mismatch caused by rounding
    if env.size < n:
        env = np.concatenate([env, np.full(n - env.size, env[-1])])
    else:
        env = env[:n]

    return x * env


# TODO: Replace the code below with your implementation of a FM synthesis
# Hint: You should really be doing PM.
def fm_synth(carrier_type, carrier_freq, mod_index, mod_ratio, dur, fs=44100, amp=1, modulator_type='sine'):
    try:
        dur = float(dur)
    except:
        dur = 0.0
    if dur <= 0:
        return np.array([])

    try:
        fc = float(carrier_freq)
    except:
        fc = 0.0
    try:
        I = float(mod_index)
    except:
        I = 0.0
    try:
        ratio = float(mod_ratio)
    except:
        ratio = 1.0
    try:
        amp = float(amp)
    except:
        amp = 1.0

    t = np.arange(0.0, dur, 1.0 / fs)
    if t.size == 0:
        return np.array([])

    fm = fc * ratio

    m = gen_wave(modulator_type, fm, dur, fs=fs, amp=1, phi=0)

    # If gen_wave returned slightly different length due to rounding, trim/pad
    if m.size < t.size:
        m = np.concatenate([m, np.full(t.size - m.size, m[-1] if m.size > 0 else 0.0)])
    else:
        m = m[:t.size]

    # --- Phase modulation: phase = 2π fc t + I * m(t) ---
    phase = (2.0 * np.pi * fc * t + I * m)

    # --- Carrier shaping from phase (no scipy.signal, no np.sign) ---
    if carrier_type == 'sine':
        y = np.sin(phase)

    elif carrier_type == 'square':
        s_c = np.sin(phase)
        y = (s_c >= 0).astype(float) * 2.0 - 1.0

    elif carrier_type == 'saw':
        frac_c = (phase / (2.0 * np.pi)) - np.floor(phase / (2.0 * np.pi))
        y = 2.0 * frac_c - 1.0

    elif carrier_type == 'triangle':
        frac_c = (phase / (2.0 * np.pi)) - np.floor(phase / (2.0 * np.pi))
        y = 1.0 - 4.0 * np.abs(frac_c - 0.5)

    else:
        y = np.sin(phase)

    sig = amp * y
    return sig

# TODO: Replace the code below with your implementation of a AM synthesis
def am_synth(carrier_type, carrier_freq, mod_depth, mod_ratio, dur, fs=44100, amp=1, modulator_type='sine'):
    try:
        dur = float(dur)
    except:
        dur = 0.0
    if dur <= 0:
        return np.array([])

    try:
        fc = float(carrier_freq)
    except:
        fc = 0.0
    try:
        depth = float(mod_depth)
    except:
        depth = 0.0
    if depth < 0.0:
        depth = 0.0
    if depth > 1.0:
        depth = 1.0

    try:
        ratio = float(mod_ratio)
    except:
        ratio = 1.0
    try:
        amp = float(amp)
    except:
        amp = 1.0

    t = np.arange(0.0, dur, 1.0 / fs)
    if t.size == 0:
        return np.array([])

    fm = fc * ratio

    carrier = gen_wave(carrier_type, fc, dur, fs=fs, amp=amp, phi=0)
    mod = gen_wave(modulator_type, fm, dur, fs=fs, amp=1, phi=0)

    if carrier.size < t.size:
        carrier = np.concatenate([carrier, np.full(t.size - carrier.size, carrier[-1] if carrier.size > 0 else 0.0)])
    else:
        carrier = carrier[:t.size]

    if mod.size < t.size:
        mod = np.concatenate([mod, np.full(t.size - mod.size, mod[-1] if mod.size > 0 else 0.0)])
    else:
        mod = mod[:t.size]

    mod01 = 0.5 * (mod + 1.0)
    env = (1.0 - depth) + depth * mod01

    sig = carrier * env
    return sig


# TODO: Complete at least one of the functions below: filter, reverb, delay.

# Note: I wrote this to only create low or highpass filters. You can alter to create bandpass/bandstop, but do not change the function definition.
def filter(data, type, cutoff_freq, fs=44100, order=5):
    """
    Args:
    data (np.array) = signal to be modified
    type (str) = filter type 'lowpass' or 'highpass'
    cutoff_freq (float) = cutoff frequency in Hz
    fs (float) = sampling frequency of the sinusoid in Hz
    order (int) = filter order

    Returns:
    The function should return a numpy array
    sig (numpy array) = filtered signal
    """
    sig = data
    return sig

def reverb(data, ir, dry_wet=0.5):
    """
    Args:
    data (np.array) = signal to be modified
    ir (str) = file path to impulse response
    dry_wet (float) = value between 0-1 dry/wet balance

    Returns:
    The function should return a numpy array
    sig (numpy array) = signal with reverb
    """
    sig = data
    return sig

def delay(data, delay_time, dry_wet=0.5, fs=44100):
    """
    Args:
    data (np.array) = signal to be modified
    delay_time (float) = delay time in seconds
    dry_wet (float) = value between 0-1 dry/wet balance
    fs (float) = sampling frequency of the sinusoid in Hz

    Returns:
    The function should return a numpy array
    sig (numpy array) = signal with a delay
    """
    sig = data
    return sig
