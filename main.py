from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import random, os

os.makedirs('samples', exist_ok=True)
os.makedirs('result', exist_ok=True)

string = '안녕하세요 너굴 상회입니다'
lang = 'ko'
random_factor = 0.35
normal_frame_rate = 44100

result_sound = None

for i, letter in enumerate(string):
    if letter == ' ':
        new_sound = letter_sound._spawn(b'\x00' * (44100 // 3), overrides={'frame_rate': 44100})
    else:
        # 한글자 별, 한글자 이름의 mp3 파일이 기존에 없다면
        if not os.path.isfile('samples/%s.mp3' % letter):
            # tts로 음성 파일을 만들어 저장함
            tts = gTTS(letter, lang=lang)
            tts.save('samples/%s.mp3' % letter)

        # 해당 글자의 음성파일이 있으면 불러옴
        letter_sound = AudioSegment.from_mp3('samples/%s.mp3' % letter)

        raw = letter_sound.raw_data[5000:-5000]

        octaves = 2.0 + random.random() * random_factor
        frame_rate = int(letter_sound.frame_rate * (2.0 ** octaves))
        print('%s - octaves: %.2f, fr: %.d' % (letter, octaves, frame_rate))

        new_sound = letter_sound._spawn(raw, overrides={'frame_rate': frame_rate})
    
    new_sound = new_sound.set_frame_rate(normal_frame_rate)
    result_sound = new_sound if result_sound is None else result_sound + new_sound

play(result_sound)
result_sound.export('result/%s.mp3' % string, format='mp3')
