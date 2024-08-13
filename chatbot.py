import datetime
import requests
import spacy
import re
import pyjokes
from googlesearch import search
import tkinter as tk
from tkinter import scrolledtext

nlp = spacy.load("en_core_web_sm")

def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def get_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def get_year():
    return datetime.datetime.now().strftime("%Y")

def get_month():
    return datetime.datetime.now().strftime("%B")

def get_temperature(city):
    api_key = "f8e2be4e35ae68b8c60bee1a71ef328d"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        return f"The temperature in {city} is {temperature}°C"
    else:
        return "City not found."

def get_ip():
    response = requests.get("https://api.ipify.org?format=json")
    return f"Your IP address is {response.json()['ip']}"

def get_joke():
    return pyjokes.get_joke()

def calculator(expression):
    try:
        return f"The Result is : {eval(expression)}"
    except Exception as e:
        return "Invalid expression"

def google_search(query):
    results = []
    for result in search(query, num_results=3):
        results.append(result)
    return results

def custom_chat(user_input):
    if "how are you" in user_input.lower():
        return "I'm a chatbot, so I don't have feelings, but thanks for asking!"
    elif "your name" in user_input.lower():
        return "I'm your friendly chatbot!"
    else:
        return "Sorry, I didn't understand that. Can you please rephrase?"

def chatbot(user_input):
    doc = nlp(user_input)

    if "time" in user_input.lower():
        return get_time()
    elif "date" in user_input.lower():
        return get_date()
    elif "year" in user_input.lower():
        return get_year()
    elif "month" in user_input.lower():
        return get_month()
    elif "temperature" in user_input.lower():
        city = re.search(r"temperature in (\w+)", user_input.lower())
        if city:
            return get_temperature(city.group(1))
        else:
            return "Please specify the city."
    elif "ip address" in user_input.lower():
        return get_ip()
    elif "calculate" in user_input.lower():
        expression = re.search(r"calculate (.+)", user_input.lower())
        if expression:
            return calculator(expression.group(1))
        else:
            return "Please provide an expression to calculate."
    elif "joke" in user_input.lower():
        return get_joke()
    elif "search" in user_input.lower():
        query = re.search(r"search (.+)", user_input.lower())
        if query:
            results = google_search(query.group(1))
            return "\n".join(results)
        else:
            return "Please provide a search query."
    elif "exit" in user_input.lower():
        return "Goodbye!"
    else:
        return custom_chat(user_input)

def send_message(event=None):
    user_input = user_entry.get()
    chat_window.insert(tk.END, "You: " + user_input + "\n", 'user')
    response = chatbot(user_input)
    
    if isinstance(response, int) or isinstance(response, float):
        response = str(response)
    
    chat_window.insert(tk.END, "Bot: " + response + "\n", 'bot')
    user_entry.delete(0, tk.END)
    if "goodbye" in response.lower():
        root.quit()

def exit_chat():
    root.quit()


root = tk.Tk()
root.title("Chatbot")
root.geometry("500x600")
root.configure(bg='#add8e6')


pre_greeting = "Hello! I am your friendly chatbot. How can I assist you today?\n"
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg='#f0f8ff', font=('Arial', 12))
chat_window.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
chat_window.tag_config('user', foreground='blue')
chat_window.tag_config('bot', foreground='green')
chat_window.insert(tk.END, pre_greeting, 'bot')


user_entry = tk.Entry(root, width=50, font=('Arial', 12))
user_entry.pack(pady=10, padx=10)
user_entry.bind("<Return>", send_message)  


button_frame = tk.Frame(root, bg='#add8e6')
button_frame.pack(pady=10)


send_button = tk.Button(button_frame, text="Send", command=send_message, bg='#90ee90', font=('Arial', 12))
send_button.grid(row=0, column=0, padx=5)


exit_button = tk.Button(button_frame, text="Exit", command=exit_chat, bg='#ff6347', font=('Arial', 12))
exit_button.grid(row=0, column=1, padx=5)


root.mainloop()
