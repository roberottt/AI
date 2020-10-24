import speech_recognition as s

r = s.Recognizer()

with s.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    data = r.record(source, duration=5)
    text = r.recognize_google(data,language='es')
    print(text)