import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import multiprocessing
import os
import logging

# LOGGING
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    filename='logs.log',
                    filemode='w')

# LOAD ENVIRONMENT VARIABLES
load_dotenv()

# URLS
URLS = {
    "muhendislik": "https://muhendislik.mcbu.edu.tr/duyurular.22.tr.html",
    "bilgisayar": "https://bilgisayarmuh.mcbu.edu.tr/default.aspx"
}

# EMAIL INFO
EMAIL_INFO = {
    "sender_email": "baranenglando@gmail.com",
    "sender_password": os.getenv("sender_password"),
    "receiver_emails": ["baran200167@gmail.com","karac.yusuf1@gmail.com","sametkizil22@gmail.com","aliatabak2@gmail.com"]
}

# Function that creates email
def create_email(title, content):
    message = MIMEMultipart()
    message['Subject'] = title
    message['From'] = EMAIL_INFO["sender_email"]
    message['To'] = ", ".join(EMAIL_INFO["receiver_emails"])
    body = content
    message.attach(MIMEText(body, 'plain'))
    return message.as_string()

# Function that checks announcements
def check_announcements(url_key):
    url = URLS[url_key]
    previous_content = ""
    while True:
        logging.info(f"{url_key.upper()} sayfasi duyurulari kontrol ediliyor.....")
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            if url_key == "muhendislik":
                table = soup.find("table", attrs={"class": "dxdvControl_None"})
                rows = table.find_all("td", attrs={"class": "dxdvItem_None"})
                latest_header = rows[0].find("h3").find_all("a")[1].text
                latest_content = rows[0].find("p").text.strip()
                latest_content_link = rows[0].find("h3").find_all("a")[1]["href"]
            elif url_key == "bilgisayar":
                data_divs = soup.find("div", attrs={"id": "sc1"})
                data_divs_list = data_divs.find("ul")
                rows = data_divs_list.find_all("li", attrs={"class": "CustomLi"})

                latest_header = rows[0].find("h4", attrs={"class":"CustomLiHeader"}).text.strip()
                latest_content = rows[0].find("p", attrs={"class":"CustomLiP"}).text.strip()
                latest_content_link = rows[0].find("a")["href"]

            if previous_content != latest_content:
                logging.info(f"----------------------------------------------------")
                logging.info(f"{url_key.upper()} sayfasinda yeni bir duyuru var.")
                logging.info(f"Baslik: {latest_header.encode('utf-8').decode('utf-8')}")
                logging.info(f"Icerik: {latest_content.encode('utf-8').decode('utf-8')}")
                logging.info(f"Link  : {latest_content_link.encode('utf-8').decode('utf-8')}")
                logging.info(f"----------------------------------------------------")
                email_title = f"{url_key.upper()} sayfasinda yeni bir duyuru var: {latest_content}"
                email_content = f"{latest_header}\n{latest_content}\n{latest_content_link}"
                email = create_email(email_title, email_content)
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(EMAIL_INFO["sender_email"], EMAIL_INFO["sender_password"])
                    server.sendmail(EMAIL_INFO["sender_email"], EMAIL_INFO["receiver_emails"], email)
                previous_content = latest_content
                time.sleep(300)
        except Exception as e:
            logging.error(f"{url_key.upper()} sayfasi duyurulari kontrol edilirken hata olustu: {e}")
            time.sleep(60)
            continue
        

if __name__ == "__main__":
    
    processes = []
    for url_key in URLS.keys():
        process = multiprocessing.Process(target=check_announcements, args=(url_key,))
        processes.append(process)
        process.start()
        logging.info(f"{process.name} started.")
    for process in processes:
        process.join()
        logging.info(f"{process.name} joined.")
