from vosk import Model, KaldiRecognizer
import pyaudio
import json
from image_generator import ImageGenerator
import tkinter as tk
from PIL import ImageTk
import platform

if platform.system() == 'Windows':
    from printer_win import print_image
else:
    from printer_macos import print_image


def parse_result(result):
    result = json.loads(result)
    return result.get('text', '')


def listen_for_target_string(target_string):
    print("Listening for target string...")
    model = Model(r"C:\Users\Anton\Documents\stable-diffusion\vosk\vosk-model-small-en-us-0.15")
    rec = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8000
    )
    stream.start_stream()

    while True:
        data = stream.read(2000)
        if len(data) == 0:
            break

        if rec.AcceptWaveform(data):
            result = rec.Result()
            print(result)
            text = parse_result(result)
            if target_string.lower() in text.lower():
                stream.stop_stream()
                stream.close()
                p.terminate()
                return text
        else:
            print(rec.PartialResult())

    stream.stop_stream()
    stream.close()
    p.terminate()
    return ""


def display_image(image):
    # Create a window using tkinter
    root = tk.Tk()
    root.title("Generated Image")

    # Convert the PIL image to a format tkinter can use
    img = ImageTk.PhotoImage(image)

    # Create a label widget to hold the image
    panel = tk.Label(root, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")

    # Start the GUI event loop
    root.mainloop()


def main():
    print("Load image generator")
    generator = ImageGenerator()
    target_string = "i want"

    while True:
        # Listen for the target string
        text = listen_for_target_string(target_string)

        # If target string is received, generate and print image
        if text:
            images = generator.generate_image(text)
            # Assume images is a list of images, take the first element
            image = images[0]
            # Print the image with the recognized text below

            #print_image(image, text)
            display_image(image)
            print("Image printed. Restarting listening...")


if __name__ == "__main__":
    main()
