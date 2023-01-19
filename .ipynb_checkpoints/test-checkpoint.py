# import streamlit as st
# st.text_area("Taper ici")
# st.sidebar.header("Menu")
# st.date_input("La date")
# st.time_input("Time")
# st.color_picker("Color:")

# import schedule
# import time

# def dire_bonjour():
#     print("Bonjour, le monde !")
    
# schedule.every(5).seconds.do(dire_bonjour)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

import requests
from bs4 import BeautifulSoup

url = "https://www.agoda.com/city/brazzaville-cg.html?cid=1844104"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

hotels = soup.find_all('div', class_="DatelessPropertyCard")

for hotel in hotels:
    name = hotel.find('div', class_="DatelessPropertyCard__ContentHeader").text
    print(name)
    break