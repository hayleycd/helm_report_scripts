import sys
import os
import urllib.request as open_url
from bs4 import BeautifulSoup

def return_data(my_url, my_class):
    my_http_response = open_url.urlopen(my_url)
    soup = BeautifulSoup(my_http_response.read())
    my_data = []
    for each in soup.find_all('a'):
        each_title = each.get("title", None)
        each_class = each.get("class", None)
        if (each_title != None) and (each_class[0] == my_class):
            my_data.append(each_title)
    
    return my_data