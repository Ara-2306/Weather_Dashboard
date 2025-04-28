import requests
import tkinter as tk
from tkinter import messagebox, font as tkFont, scrolledtext
import speech_recognition as sr
import subprocess
import threading

API_KEY = 'your_real_api_key_here'
MODEL_NAME = 'llama3.2:latest'
PLACEHOLDER_TEXT = "Enter city name..."
BASE_FONT_SIZE = 12
TITLE_FONT_SIZE = 18
RESULT_FONT_SIZE = 13

# Global to store last fetched weather
last_weather = None

def get_weather(city):
    city_lower = city.lower()
    dummy_data = {
        "mumbai": {"city": "Mumbai", "temp": 32, "humidity": 70, "description": "Sunny", "wind": 4.5},
        "pune":   {"city": "Pune",   "temp": 26, "humidity": 60, "description": "Partly Cloudy", "wind": 3.2}
    }
    if city_lower in dummy_data:
        messagebox.showinfo("Info", f"Showing local data for {city.capitalize()} (Not fetched from API). 😉")
        return dummy_data[city_lower]

    if API_KEY == 'your_real_api_key_here':
        messagebox.showwarning("API Key Missing", 
            "Replace API_KEY with your OpenWeatherMap key to fetch live data.")
        return None

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url, timeout=10)
    data = response.json()
    return {
        "city": data.get("name", city.capitalize()),
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"].title(),
        "wind": data["wind"]["speed"]
    }

def get_mood_suggestion(weather):
    desc = weather['description'].lower()
    temp = weather['temp']
    if 'rain' in desc or 'drizzle' in desc:
        return "Perfect time for chai and a playlist. ☕🎶"
    if temp > 30:
        return "Wear something light — it’s hot out there! 🔥"
    if temp < 15:
        return "Snuggle up with a warm blanket and hot cocoa. ❄️☕"
    if 'cloud' in desc:
        return "A walk under the overcast sky sounds poetic. ☁️🚶‍♂️"
    if 'clear' in desc or 'sun' in desc:
        return "It's a beautiful day! Go out and shine. ✨"
    return "Enjoy the weather today! 👍"

def auto_clothing_advice():
    """Automatically ask the LLM for clothing advice based on last_weather."""
    if not last_weather:
        return

    ctx = (
        f"{last_weather['city']}: {last_weather['description']}, "
        f"{last_weather['temp']}°C, Humidity {last_weather['humidity']}%, "
        f"Wind {last_weather['wind']} m/s"
    )
    prompt = (
        "You are a fashion-savvy assistant. Suggest what to wear based on the weather context below.\n"
        f"Context: {ctx}\n\n"
        "Outfit Advice:"
    )

    proc = subprocess.Popen(
        ["ollama", "run", MODEL_NAME],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    resp, err = proc.communicate(prompt)
    advice = resp.strip() if resp else f"[Ollama Error] {err.strip()}"

    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"AI (Clothing Advice): {advice}\n\n")
    chat_history.config(state=tk.DISABLED)
    chat_history.see(tk.END)

def display_weather_results():
    global last_weather
    city = city_entry.get().strip()
    if not city or city == PLACEHOLDER_TEXT:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    result_label.config(text="Fetching weather...")
    root.update_idletasks()

    weather = get_weather(city)
    last_weather = weather
    if weather:
        mood = get_mood_suggestion(weather)
        output = (
            f"City: {weather['city']}\n"
            f"Temperature: {weather['temp']} °C\n"
            f"Weather: {weather['description']}\n"
            f"Humidity: {weather['humidity']}%\n"
            f"Wind Speed: {weather['wind']} m/s\n\n"
            f"Mood Suggestion: {mood}"
        )
        result_label.config(text=output)
        # Fire-and-forget advice
        threading.Thread(target=auto_clothing_advice, daemon=True).start()
    else:
        result_label.config(text="Could not retrieve weather data.")

def handle_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Input", "Listening... Speak the city name clearly. 🎤")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        city = recognizer.recognize_google(audio)
        city_entry.config(fg='black')
        city_entry.delete(0, tk.END)
        city_entry.insert(0, city)
        messagebox.showinfo("Voice Input", f"Recognized: {city}. Fetching weather...")
        display_weather_results()

def send_chat():
    user_msg = chat_entry.get().strip()
    if not user_msg:
        return

    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"You: {user_msg}\n")
    chat_history.config(state=tk.DISABLED)
    chat_entry.delete(0, tk.END)

    # Build weather context if available
    if last_weather:
        ctx = (
            f"{last_weather['city']} - {last_weather['description']}, "
            f"{last_weather['temp']}°C, Humidity {last_weather['humidity']}%, "
            f"Wind {last_weather['wind']} m/s"
        )
    else:
        ctx = "No weather data available."

    prompt = (
        "You are a helpful weather-savvy assistant.\n"
        f"Context: {ctx}\n\n"
        f"User: {user_msg}\n"
        "AI:"
    )

    proc = subprocess.Popen(
        ["ollama", "run", MODEL_NAME],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    resp, err = proc.communicate(prompt)
    ai_response = resp.strip() if resp else f"[Ollama Error] {err.strip()}"

    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"AI: {ai_response}\n\n")
    chat_history.config(state=tk.DISABLED)
    chat_history.see(tk.END)

def handle_entry_focus(event):
    w = event.widget
    if w.get() == PLACEHOLDER_TEXT and event.type == tk.EventType.FocusIn:
        w.delete(0, tk.END); w.config(fg='black')
    elif not w.get() and event.type == tk.EventType.FocusOut:
        w.insert(0, PLACEHOLDER_TEXT); w.config(fg='grey')

# --- GUI Setup ---
root = tk.Tk()
root.title("AI Weather Dashboard 🌤️🤖 (Chat-Ready Normal)")
root.minsize(500, 600)
root.configure(bg="#e0f7fa")

default_font = tkFont.Font(family="Helvetica", size=BASE_FONT_SIZE)
title_font   = tkFont.Font(family="Helvetica", size=TITLE_FONT_SIZE, weight="bold")
result_font  = tkFont.Font(family="Consolas",   size=RESULT_FONT_SIZE)
button_font  = tkFont.Font(family="Helvetica",  size=BASE_FONT_SIZE, weight="bold")

tk.Label(root, text="Weather Dashboard 🌤️", font=title_font, bg="#e0f7fa", fg="#01579b")\
    .pack(pady=(15,10), padx=10, fill="x")

city_entry = tk.Entry(root, font=default_font, fg="grey", bd=2, relief="groove")
city_entry.pack(pady=5, padx=20, fill="x")
city_entry.insert(0, PLACEHOLDER_TEXT)
city_entry.bind("<FocusIn>", handle_entry_focus)
city_entry.bind("<FocusOut>", handle_entry_focus)

btn_frame = tk.Frame(root, bg="#e0f7fa"); btn_frame.pack(pady=10)
tk.Button(btn_frame, text="Get Weather", command=display_weather_results,
          bg="#4db6ac", activebackground="#26a69a",
          font=button_font, fg="white", relief="raised", padx=10, pady=3, width=12)\
    .grid(row=0, column=0, padx=10)

result_label = tk.Label(root, text="", font=result_font, justify=tk.LEFT, anchor="nw",
                        bg="#ffffff", fg="#333333", wraplength=450,
                        padx=15, pady=15, bd=1, relief="solid")
result_label.pack(padx=20, pady=(5,15), fill="both", expand=True)

chat_frame = tk.LabelFrame(root, text="Chat with AI", font=default_font, bg="#e0f7fa")
chat_frame.pack(padx=20, pady=(0,15), fill="both", expand=True)

chat_history = scrolledtext.ScrolledText(chat_frame, state=tk.DISABLED, wrap=tk.WORD, font=default_font)
chat_history.pack(padx=10, pady=10, fill="both", expand=True)

chat_entry = tk.Entry(chat_frame, font=default_font)
chat_entry.pack(side=tk.LEFT, padx=(10,0), pady=(0,10), fill="x", expand=True)
chat_entry.bind("<Return>", lambda e: send_chat())

tk.Button(chat_frame, text="Send", command=send_chat,
          font=button_font, fg="white", relief="raised", padx=10, pady=3)\
    .pack(side=tk.RIGHT, padx=10, pady=(0,10))

root.eval('tk::PlaceWindow . center')
root.focus_set()
root.mainloop()