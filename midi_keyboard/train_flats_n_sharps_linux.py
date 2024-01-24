#!/usr/bin/python3
import random
import mido
import pyttsx3
import time

iterations=32

NOTES_SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTES_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

EQUAL_NOTES = [['C#', 'Db'], ['D#', 'Eb'], ['F#', 'Gb'], ['G#', 'Ab'], ['A#', 'Bb']]

def get_note_from_midi(midi_number):
    if not (0 <= midi_number <= 127):
        print('MIDI number out of range (0-127)')
        return None

    octave = (midi_number // 12) - 1
    note_index = midi_number % 12

    # Determine whether to use sharp or flat based on the note index
    sharp_note = NOTES_SHARP[note_index]
    flat_note = NOTES_FLAT[note_index]

    return sharp_note, flat_note

def get_random_note():
    return random.choice(NOTES_SHARP + NOTES_FLAT)

def are_notes_equal(note1, note2):
    if note1 == note2:
        return True
    return [note1, note2] in EQUAL_NOTES or [note2, note1] in EQUAL_NOTES

# Use pyttsx3 for text-to-speech on Linux
speaker = pyttsx3.init()
out_port = mido.open_output()

# Adjust the input port name based on your MIDI device
input_port_name = "Digital Keyboard MIDI 1"

with mido.open_input(input_port_name) as inport:
    start_time = time.time()
    counter = 0
    previous_note=note_to_guess=""
    while True:
        while are_notes_equal(previous_note, note_to_guess):
            note_to_guess = get_random_note()
        previous_note=note_to_guess
        if '#' in note_to_guess:
            suffix = 'Sharp'
        elif 'b' in note_to_guess:
            suffix = 'Flat'
        else:
            suffix = ''
        print(f"{note_to_guess[0]} {suffix}")
        speaker.say(f"{note_to_guess[0]} {suffix}")
        speaker.runAndWait()
        first_loop=True
        for msg in inport:
            if msg.type == 'note_on':
                received_sharp, received_flat = get_note_from_midi(msg.note)
                if received_sharp.upper() == note_to_guess.upper() or received_flat.upper() == note_to_guess.upper():
                    #correct_note_received
                    break
                elif first_loop:
                    first_loop=False
                else:
                    print('Wrong!')
                    counter=0

        counter += 1
        if counter > iterations:
            end_time = time.time()
            interval_seconds = end_time - start_time
            speaker.say(f'Congratulations, it took you {int(interval_seconds)} seconds!')
            speaker.runAndWait()
            print(f'Congratulations, it took you {int(interval_seconds)} seconds!')
            quit()

