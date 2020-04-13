import pydub.scipy_effects
from pydub import AudioSegment
# from pydub.playback import play

# raw = AudioSegment.from_wav("blah.wav")
# six = pydub.scipy_effects.low_pass_filter(raw, 6000, order=1)

# play(raw)
# play(six)
# six._data

def bandstop(seg, low, high, order=2):
    filter_fn = pydub.scipy_effects._mk_butter_filter([low, high], 'bandstop', order=order)
    return seg.apply_mono_filter_to_each_channel(filter_fn)

def de_esser(seg):
    return bandstop(seg, 7000, 11000, order=4)
