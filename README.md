# ⚡ Pulse Bot

An automated multi-task background engine powered by **Python** and **GitHub Actions**. Pulse Bot scrapes real-time weather and tech news data, delivers custom HTML email briefings to your inbox, and dynamically tracks public GitHub repository metadata.

---

## 🚀 Key Features

* **Task 1: Live Weather Alerts** 🌤️  
  Fetches real-time weather updates and temperatures for Kochi using the OpenWeatherMap API and emails instant condition alerts.
* **Task 2: Top Tech Headlines Briefing** 📰  
  Scrapes current top headlines across major tech news outlets using `requests` and `BeautifulSoup`, formatting them into a clean HTML briefing delivered straight to your email.
* **Task 3: Dynamic Portfolio Data Matrix** 📊  
  Queries the GitHub REST API to pull public repository stats (stars, tech stack, descriptions, updates) and automatically generates and commits `projects.json` back to the repository.

---

## 🛠️ Built With

* **Language:** Python 3.10
* **Libraries:** `requests`, `beautifulsoup4`
* **Automation Platform:** GitHub Actions (`workflow_dispatch`)
* **APIs & Data:** OpenWeatherMap API, GitHub REST API
* **Protocols:** SMTP (TLS Email Dispatch)

---

## 📂 Repository Architecture

```text
.
├── .github/
│   └── workflows/
│       └── daily.yml             # GitHub Actions automation pipeline
├── bot.py                        # Task 1: Weather alert script
├── news_bot.py                   # Task 2: Web scraping & tech news emailer
├── portfolio_updater.py          # Task 3: GitHub API parser & projects.json generator
├── projects.json                 # Dynamically updated repository matrix
└── requirements.txt              # Environment dependency manifest
<img width="189" height="1280" alt="WhatsApp Image 2026-10-15 at 01 51 40" src="https://github.com/user-attachments/assets/10f8f55d-6712-4e05-b4c1-a595674bae36" />
<img width="540" height="1170" alt="WhatsApp Image 2026-10-15 at 01 51 40 (1)" src="https://github.com/user-attachments/assets/194c1228-4a9a-47a1-8666-b7644d15b395" />
