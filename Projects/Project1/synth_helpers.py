import numpy as np
from scipy.io.wavfile import read, write
from scipy import signal
from scipy.signal import square, sawtooth



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
import numpy as np

def adsr(data, attack, decay, sustain_level, release, fs=44100):
    try:
        attack + decay + sustain_level + release
    except:
        raise ValueError("ADSR parameters must be numeric.")

    if sustain_level < 0 or sustain_level > 1:
        raise ValueError("Sustain level must be between 0 and 1.")

    N = len(data)
    if N == 0:
        return data

    # scale if A + D + R exceed 100%
    total = attack + decay + release
    if total > 100:
        scale = 100.0 / total
        attack *= scale
        decay *= scale
        release *= scale

    # convert percent → sample counts
    a_n = int((attack/100.0) * N)
    d_n = int((decay/100.0) * N)
    r_n = int((release/100.0) * N)
    s_n = N - (a_n + d_n + r_n)

    # fix negative sustain length
    if s_n < 0:
        s_n = 0
        r_n = max(0, r_n)
        d_n = max(0, d_n)
        a_n = max(0, a_n)

    # build envelope
    a = np.linspace(0, 1, a_n, endpoint=False)
    d = np.linspace(1, sustain_level, d_n, endpoint=False)
    s = np.full(s_n, sustain_level)
    r = np.linspace(sustain_level, 0, r_n)

    env = np.concatenate((a, d, s, r))

    # fix rounding mismatch
    if len(env) != N:
        env = env[:N]

    return data * env


# TODO: Replace the code below with your implementation of a FM synthesis
# Hint: You should really be doing PM.

def fm_synth(carrier_type, carrier_freq, mod_index, mod_ratio, dur, fs=44100, amp=1, modulator_type='sine'):

    try:
        carrier_freq + mod_index + mod_ratio + dur + fs + amp
    except:
        raise ValueError("carrier_freq, mod_index, mod_ratio, dur, fs, and amp must be numeric.")

    if fs <= 0 or dur <= 0 or carrier_freq < 0:
        return np.array([], dtype=float)

    # sanitize strings
    try:
        carrier = carrier_type.lower()
    except:
        carrier = 'sine'
    try:
        modulator = modulator_type.lower()
    except:
        modulator = 'sine'

    # core parameters
    N = int(dur * fs)
    if N <= 0:
        return np.array([], dtype=float)
    t = np.arange(N, dtype=float) / float(fs)

    # modulator
    fm = carrier_freq * mod_ratio
    arg_m = 2.0 * np.pi * fm * t
    if modulator == 'square':
        m = square(arg_m)
    elif modulator in ('saw', 'sawtooth'):
        m = sawtooth(arg_m)
    elif modulator in ('tri', 'triangle'):
        m = sawtooth(arg_m, 0.5)  # triangle
    else:
        m = np.sin(arg_m)  # sine default

    # phase for PM
    phase = 2.0 * np.pi * carrier_freq * t + (mod_index * m)

    # carrier waveform
    if carrier == 'square':
        y = amp * square(phase)
    elif carrier in ('saw', 'sawtooth'):
        y = amp * sawtooth(phase)
    elif carrier in ('tri', 'triangle'):
        y = amp * sawtooth(phase, 0.5)  # triangle
    else:
        y = amp * np.sin(phase)  # sine default

    return y


# TODO: Replace the code below with your implementation of a AM synthesis
def am_synth(carrier_type, carrier_freq, mod_depth, mod_ratio, dur, fs=44100, amp=1, modulator_type='sine'):

    try:
        carrier_freq + mod_depth + mod_ratio + dur + fs + amp
    except:
        raise ValueError("carrier_freq, mod_depth, mod_ratio, dur, fs, and amp must be numeric.")

    if fs <= 0 or dur <= 0 or carrier_freq < 0:
        return np.array([], dtype=float)

    # sanitize type strings
    try:
        carrier = carrier_type.lower()
    except:
        carrier = 'sine'
    try:
        modulator = modulator_type.lower()
    except:
        modulator = 'sine'

    # clamp modulation depth to [0, 1]
    if mod_depth < 0:
        mod_depth = 0.0
    if mod_depth > 1:
        mod_depth = 1.0

    # core params
    N = int(dur * fs)
    if N <= 0:
        return np.array([], dtype=float)
    t = np.arange(N, dtype=float) / float(fs)

    # modulator frequency and waveform (in [-1, 1])
    fm = carrier_freq * mod_ratio
    arg_m = 2.0 * np.pi * fm * t
    if modulator == 'square':
        m = square(arg_m)
    elif modulator in ('saw', 'sawtooth'):
        m = sawtooth(arg_m)
    elif modulator in ('tri', 'triangle'):
        m = sawtooth(arg_m, 0.5)  # triangle
    else:
        m = np.sin(arg_m)

    # amplitude envelope in [1 - mod_depth, 1]
    env = (1.0 - mod_depth) + mod_depth * (m + 1.0) * 0.5

    # carrier waveform
    phase_c = 2.0 * np.pi * carrier_freq * t
    if carrier == 'square':
        c = square(phase_c)
    elif carrier in ('saw', 'sawtooth'):
        c = sawtooth(phase_c)
    elif carrier in ('tri', 'triangle'):
        c = sawtooth(phase_c, 0.5)  # triangle
    else:
        c = np.sin(phase_c)

    return amp * env * c

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
