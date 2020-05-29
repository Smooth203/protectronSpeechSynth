from g2p_en import G2p
from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import normalize
from random import *
import math
import os



#load phons
phonemes= {}
print("Loading phonemes")
for i, file in enumerate(os.listdir("speech/phonemes/")):
    phon = file[:-4]
    phonemes[phon] = AudioSegment.from_wav("speech/phonemes/"+file)
    print("Loading Speech: " + str(math.floor((i/len(os.listdir("speech/phonemes/")))*100))+"%")

print("Finished Loading")

def say(text):
    #converts text to phonemes
    if(text == 'QUIT'):
        exit()
    g2p = G2p()
    out = g2p(text)

    #identify sounds from phoneme name

    output = AudioSegment.empty()

    for i, pho in enumerate(out):
        if (pho == 'HH'):
            pho = 'H'
        elif (pho == 'NX'):
            pho = 'NG'
        elif (pho == 'TH'):
            pho = 'DH'

        if (pho[-1].isalpha() != True):
            pho = pho[:-1]

        if (out[i].isspace() or out[i] == '' or out[i] == "'" or out[i] == "-" or out[i] =='.' or out[i] == ',' or out[i] == '!' or out[i] == '?'):
            audio = AudioSegment.silent(duration=300)
            audio.fade_in(duration=300).fade_out(duration=300)
            output = output.append(audio, crossfade=10)
        else:
            phonemes[pho]= phonemes[pho].fade_in(duration=5)
            phonemes[pho] = phonemes[pho].fade_out(duration=5)
            phonemes[pho] = normalize(phonemes[pho])
            output = output.append(phonemes[pho], crossfade=0) # 
    
    output += AudioSegment.silent(duration=300)
    output = normalize(output)
    output.set_frame_rate(44100)

    play(output)
    print(text)