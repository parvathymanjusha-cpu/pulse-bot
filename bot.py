import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
import requests

def get_weather(city="Thiruvananthapuram"):
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        return f"Weather unavailable ({e})"

def get_quote():
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return f'"{data[0]["q"]}" - {data[0]["a"]}'
    except Exception as e:
        return f"Quote unavailable ({e})"

def get_history_fact():
    url = "https://history.muffinlabs.com/date"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        event = data["data"]["Events"][0]
        return f"In {event['year']}: {event['text']}"
    except Exception as e:
        return f"Historical event unavailable ({e})"

def build_summary():
    today = datetime.today().strftime("%A, %d %B %Y")
    return f"""------------------------------------
PULSE - Daily Summary
{today}
====================================

🌦️ WEATHER
{get_weather()}

💭 TODAY'S QUOTE
{get_quote()}

📜 THIS DAY IN HISTORY
{get_history_fact()}

------------------------------------"""

def send_email(summary_text):
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")
    receiver = os.environ.get("EMAIL_RECEIVER")
    
    if not sender or not password or not receiver:
        print("ℹ️ Email secrets not configured yet. Skipping email delivery.")
        return

    msg = MIMEText(summary_text)
    msg["Subject"] = "Pulse 🌟 Daily Summary"
    msg["From"] = sender
    msg["To"] = receiver
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
            print("🚀 Email dispatched successfully!")
    except Exception as e:
        print(f"❌ Email delivery failed: {e}")

def run():
    summary = build_summary()
    print(summary)
    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    send_email(summary)
    print("Pulse executed successfully.")

if __name__ == "__main__":
    run()
    import os
import requests
import smtplib
from email.mime.text import MIMEText

# 1. Setup configurations
API_KEY = os.environ.get("OPENWEATHER_API_KEY")
CITY = "Kochi"  
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

def check_weather_and_alert():
    try:
        # 2. Fetch data from OpenWeatherMap API
        response = requests.get(URL).json()
        
        # Extract temperature and weather condition
        temp = response["main"]["temp"]
        weather_desc = response["weather"][0]["main"].lower()
        
        print(f"Current temperature in {CITY}: {temp}°C, Condition: {weather_desc}")

        # 3. Check conditions: Lowered temperature threshold to force alert email
        if temp > 15 or "rain" in weather_desc or "drizzle" in weather_desc:
            send_weather_alert(temp, weather_desc)
            print("Alert condition met. Email sent!")
        else:
            print("Weather is normal. No alert needed today.")

    except Exception as e:
        print(f"Error fetching weather data: {e}")

def send_weather_alert(temp, condition):
    # Setup Email credentials from GitHub Secrets
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")
    receiver = os.environ.get("EMAIL_RECEIVER")

    subject = f"⚠️ WEATHER ALERT: Critical Updates for {CITY}"
    body = f"Hello!\n\nThis is an automated alert from your Pulse Bot.\n\n" \
           f"Current conditions in {CITY} require attention:\n" \
           f"🌡️ Temperature: {temp}°C\n" \
           f"🌧️ Condition: {condition.capitalize()}\n\n" \
           f"Stay safe and plan accordingly!"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())

if __name__ == "__main__":
    check_weather_and_alert()
