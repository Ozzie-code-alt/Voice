import sys
import threading
import tkinter as tk

import speech_recognition
import pyttsx3 as tts

from neuralintents import GenericAssistant

print(speech_recognition.Microphone.list_microphone_names())
class Assistant:
    def __init__(self):
        self.recognizer = speech_recognition.Recognizer() #start instance
        self.speaker = tts.init() #the voice
        self.speaker.setProperty("rate", 150)

        self.assistant = GenericAssistant("intents.json", intent_methods={"file":self.create_file})
        self.assistant.train_model()

        self.root = tk.Tk()
        self.label = tk.Label(text="A", font=("Arial",120, "bold"))
        self.label.pack()
        threading.Thread(target=self.run_assistant).start() # run in a seperate thread
        self.root.mainloop()
    def create_file(self):
        with open("s0mefile.txt", "w") as f:
            f.write("Hello world")


    def run_assistant(self):
        while True:
            try:
                with speech_recognition.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.recognizer.listen(mic)

                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()
                    if "hello" in text: # if hey jake is 1 in audio process otherwise ignore
                        self.label.config(fg="red")
                        audio = self.recognizer.listen(mic) # await for another aaudio input
                        self.label.config(fg="green")
                        text = self.recognizer.recognize_google(audio)
                        text = text.lower()
                        if text == "stop":
                            self.speaker.say("Bye")
                            self.speaker.runAndWait()
                            self.speaker.stop()
                            self.root.destroy()
                            sys.exit()
                        else:
                            if text is not None:
                                response = self.assistant.request(text)
                                if response is not None:
                                    self.speaker.say(response)
                                    self.speaker.runAndWait()
                            self.label.config(fg="black")
            except:
                self.label.config(fg="black")
                continue


Assistant()