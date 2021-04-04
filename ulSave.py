import os
import requests

def saveIm():
    url = "http://www.digimouth.com/news/media/2011/09/google-logo.jpg"
    page = requests.get(url)
    f_name = "local.jpg"
    with open(f_name, 'wb') as f:
        f.write(page.content)
saveIm()
