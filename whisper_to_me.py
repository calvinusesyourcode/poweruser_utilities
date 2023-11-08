import sounddevice as sd
import numpy as np
from pydub import AudioSegment
import keyboard
import threading
import queue
import whisper

def record_audio(audio_queue, stop_event, samplerate=44100):
    print("Recording... Press '\\' to stop.")
    audio_data = []

    with sd.InputStream(samplerate=samplerate, channels=2, dtype='int16') as stream:
        while not stop_event.is_set():
            frame, overflowed = stream.read(samplerate)
            audio_data.append(frame)
            if overflowed:
                print("Buffer overflow! Some audio data has been lost.")
    
    audio_data = np.concatenate(audio_data, axis=0)
    audio_queue.put(audio_data)
    print("Recording stopped")

def save_audio_as_mp3(audio_data, filename, samplerate=44100):
    audio = AudioSegment(audio_data.tobytes(), frame_rate=samplerate, sample_width=audio_data.dtype.itemsize, channels=2)
    audio.export(filename, format="mp3")
    print(f"Audio saved as {filename}")

def on_keypress(e):
    if e.name == '\\':
        if not recording_event.is_set():
            recording_event.set()
            threading.Thread(target=record_audio, args=(audio_queue, stop_event)).start()
        else:
            stop_event.set()

def main():
    samplerate = 44100  # Sample rate in Hz
    keyboard.on_press(on_keypress, suppress=True)
    print("Press '\\' to start recording")
    
    recording_event.wait()
    print("Recording started. Press '\\' again to stop.")
    
    stop_event.wait()
    audio_data = audio_queue.get()
    save_audio_as_mp3(audio_data, "output.mp3", samplerate)
    keyboard.unhook_all()
    print(whisper.load_model("tiny").transcribe("output.mp3")["text"])


if __name__ == "__main__":
    recording_event = threading.Event()
    stop_event = threading.Event()
    audio_queue = queue.Queue()
    main()
