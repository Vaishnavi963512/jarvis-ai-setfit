import webbrowser
import os
import datetime

def open_app(app):
    if "chrome" in app:
        os.system("start chrome")
    elif "notepad" in app:
        os.system("notepad")
    elif "vscode" in app:
        os.system("code")

def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def search_google(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")

def get_weather(city):
    return f"Weather feature coming soon for {city}"