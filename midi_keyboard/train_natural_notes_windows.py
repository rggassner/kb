import random
import mido
import win32com.client
import time

NOTES_SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTES_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

def get_note_from_midi(midi_number):
    if not (0 <= midi_number <= 127):
        print('MIDI number out of range (0-127)')
        return None

    octave = (midi_number // 12) - 1
    note_index = midi_number % 12

    if 'b' in NOTES_FLAT[note_index]:
        note = NOTES_FLAT[note_index]
    else:
        note = NOTES_SHARP[note_index]
    return note

def get_random_flat_note():
    return random.choice(['C', 'D', 'E', 'F', 'G', 'A', 'B'])

speaker = win32com.client.Dispatch("SAPI.SpVoice")
out_port = mido.open_output()
counter = 0

with mido.open_input(mido.get_input_names()[0]) as inport:
    start_time = time.time()
    while True:
        note_to_guess = get_random_flat_note()
        speaker.Speak(note_to_guess)

        for msg in inport:
            if str(msg) != "clock time=0" and not str(msg).endswith(' velocity=0 time=0'):
                received_note = get_note_from_midi(msg.note)
                if received_note.upper() == note_to_guess.upper():
                    counter += 1
                    if counter > 10:
                        end_time = time.time()
                        interval_seconds = end_time - start_time
                        speaker.Speak(f'Congratulations, it took you {int(interval_seconds)} seconds!')
                        print(f'Congratulations, it took you {int(interval_seconds)} seconds!')
                        quit()
                    break
                else:
                    speaker.Speak("Wrong!"+note_to_guess)
                    counter = 0
