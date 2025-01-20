import pyaudio
import wave
import numpy as np

# Asetukset
CHUNK = 1024  # Näytteen koko
FORMAT = pyaudio.paInt16  # Äänen muoto
CHANNELS = 1  # Monokanava (mono)
RATE = 44100  # Näytteenottotaajuus
THRESHOLD = 50  # Äänenvoimakkuuden kynnysarvo (desibeleissä)
OUTPUT_FILE = "recorded_audio.wav"

def db_from_rms(rms):
    """Laskee desibeliarvon RMS:stä."""
    return 20 * np.log10(rms) if rms > 0 else -float('inf')

def main():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Kuunnellaan ääntä... Aloita äänen tuottaminen ylittääksesi kynnyksen.")

    frames = []
    recording = False

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            rms = np.sqrt(np.mean(audio_data**2))  # Root Mean Square
            db = db_from_rms(rms)

            print(f"Äänenvoimakkuus: {db:.2f} dB", end='\r')

            if db > THRESHOLD and not recording:
                print("\nTallennus aloitettu.")
                recording = True

            if recording:
                frames.append(data)
                if db <= THRESHOLD:
                    print("\nTallennus lopetettu.")
                    break

    except KeyboardInterrupt:
        print("\nKeskeytettiin käyttäjän toimesta.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

        if frames:
            print("Tallennetaan tiedosto...")
            wf = wave.open(OUTPUT_FILE, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            print(f"Tallennettu tiedosto: {OUTPUT_FILE}")
        else:
            print("Ei tallennettavaa ääntä.")

if __name__ == "__main__":
    main()
