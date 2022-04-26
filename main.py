import requests
from bs4 import BeautifulSoup

YEAR = input("What year do you want to time travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{YEAR}/"
response = requests.get(url=URL)
website = response.text

soup = BeautifulSoup(website, "html.parser")
songs = soup.findAll(name="h3", class_='c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only')


song_list = [song.getText().strip() for song in songs]
print(song_list)


