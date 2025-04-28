AI-Powered Weather Dashboard 🌤️🤖
An interactive desktop application that fetches real-time weather updates, gives mood-based suggestions, fashion advice using an AI model, and allows chatting with an AI assistant — all packed inside a beautiful Tkinter GUI!

✨ Features :
1. 🌦️ Fetch weather details by typing or speaking the city name.
2. 😍 Mood-based suggestions based on weather conditions.
3. 👗 Fashion outfit advice using a local LLM (Ollama model).
4. 🗣️ Voice input support using Speech Recognition.
5. 💬 Chat with an AI assistant for custom queries.
6. 🖥️ Clean and responsive GUI made with Tkinter and ScrolledText.

🛠️ Technologies Used : 
1. Python 3.8+
2. Tkinter (for GUI)
3. Requests (for weather API)
4. SpeechRecognition (for voice input)
5. Subprocess (to interact with Ollama LLM locally)

🗂️ Project Structure :
bash
Copy
Edit
📁 ai-weather-dashboard :
 ├── main.py          # Main application file
 ├── README.md        # (This file)
 └── requirements.txt # (Recommended to create)
⚙️ Setup Instructions
Clone this Repository

bash
Copy
Edit
git clone https://github.com/your-username/ai-weather-dashboard.git
cd ai-weather-dashboard
Install the Required Python Packages

bash
Copy
Edit
pip install requests tkinter SpeechRecognition
(Optional) Install Ollama

Ollama must be installed and running locally to use the LLM integration. Visit Ollama's official site for installation instructions.

Add Your OpenWeatherMap API Key

Open main.py and replace:

python
Copy
Edit
API_KEY = 'your_real_api_key_here'
with your actual API key from OpenWeatherMap.

Run the Application : 
bash
Copy
Edit
python main.py

📋 Notes :
1. Without Ollama: The application still works for weather and mood suggestions but skips AI clothing advice and chat features.
2. Without API Key: It will show dummy data for Mumbai and Pune with a warning.
3. Voice Input: Requires microphone access and internet connection (uses Google Web Speech API).

💡 Future Improvements : 
1. Adding multiple language support (Hindi/Marathi).
2. Weather-based dynamic wallpapers.
3. Offline LLM fallback if Ollama not detected.
4. Packaging as a standalone EXE for easy distribution.

🤝 Contributing
Pull requests are welcome! Feel free to open issues or suggest features.
Pyaar se contribute karo, gussa allowed nahi. 💖

📜 License
This project is licensed under the MIT License.

🔥 What Else to Upload?

File	Status	Notes
main.py	✅ Must Upload	Main working code.
README.md	✅ Must Upload	This file, copy-paste this content.
requirements.txt	⚡ Recommended	List all Python packages used.
/screenshots/	💖 Nice to Have	GUI screenshots for README.
LICENSE	✅ Must Upload	(Preferably MIT license.)
