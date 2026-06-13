import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

def fetch_hacker_news():
    articles = []
    try:
        res = requests.get("https://news.ycombinator.com/", timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.storylink') if soup.select('.storylink') else soup.select('.titleline > a')
        for link in links[:3]:
            articles.append({"title": link.text, "url": link['href'], "source": "Hacker News"})
    except Exception as e:
        print(f"Error fetching HN: {e}")
    return articles

def fetch_bbc_tech():
    articles = []
    try:
        res = requests.get("https://www.bbc.com/news/technology", timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        # Simple extraction for top links
        for link in soup.find_all('a', href=True):
            if "/news/technology-" in link['href'] and len(link.text.strip()) > 20:
                full_url = f"https://www.bbc.com{link['href']}" if not link['href'].startswith('http') else link['href']
                articles.append({"title": link.text.strip(), "url": full_url, "source": "BBC Tech"})
                if len(articles) >= 3: break
    except Exception as e:
        print(f"Error fetching BBC: {e}")
    return articles

def fetch_techcrunch():
    articles = []
    try:
        res = requests.get("https://techcrunch.com/", timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        for link in soup.find_all('a', {'class': 'loop-card__title-link'}, href=True)[:3]:
            articles.append({"title": link.text.strip(), "url": link['href'], "source": "TechCrunch"})
    except Exception as e:
        # Fallback if class structural layout changed slightly
        for link in soup.find_all('a', href=True):
            if "techcrunch.com/202" in link['href'] and len(link.text.strip()) > 25:
                articles.append({"title": link.text.strip(), "url": link['href'], "source": "TechCrunch"})
                if len(articles) >= 3: break
    return articles

def send_html_email(all_articles):
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")
    receiver = os.environ.get("EMAIL_RECEIVER")
    
    current_time = datetime.now().strftime("%d %B %Y, %I:%M %p")
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"📰 Top Tech Headlines Briefing - {datetime.now().strftime('%d %b')}"
    msg["From"] = sender
    msg["To"] = receiver

    # Elegant HTML layout for the presentation portal
    html = f"""
    <html>
      <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; line-height: 1.6; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
          <h2 style="margin: 0;">Daily Executive Briefing</h2>
          <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 14px;">Compiled at {current_time}</p>
        </div>
        <div style="padding: 20px; border: 1px solid #ddd; border-top: none; border-radius: 0 0 8px 8px; background-color: #f9f9f9;">
    """
    
    for item in all_articles:
        html += f"""
          <div style="margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px dashed #ddd;">
            <span style="background-color: #e1ecf4; color: #39739d; padding: 3px 8px; font-size: 11px; font-weight: bold; border-radius: 3px; text-transform: uppercase;">{item['source']}</span>
            <h4 style="margin: 8px 0 4px 0;"><a href="{item['url']}" style="color: #1e3c72; text-decoration: none; font-size: 16px;">{item['title']}</a></h4>
            <a href="{item['url']}" style="font-size: 12px; color: #888; word-break: break-all;">{item['url']}</a>
          </div>
        """
        
    html += """
        </div>
        <p style="text-align: center; font-size: 11px; color: #aaa; margin-top: 20px;">Automated Bot Delivery Platform via GitHub Actions</p>
      </body>
    </html>
    """
    
    msg.attach(MIMEText(html, "html"))
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())

if __name__ == "__main__":
    print("Scraping media networks...")
    news_feed = fetch_hacker_news() + fetch_bbc_tech() + fetch_techcrunch()
    if news_feed:
        print(f"Successfully compiled {len(news_feed)} items. Sending HTML Email...")
        send_html_email(news_feed)
        print("Briefing delivered successfully!")
    else:
        print("No articles compiled.")