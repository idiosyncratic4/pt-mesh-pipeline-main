import os
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import csv
import string
from datetime import datetime
import time
import requests
import helper_function

def get_all_links(url, session_token):
    link_list = set()
    tender_link = set()
    try:
        print('get_all_links started successfully')
        request1 = Request(url, headers={'Cookie': f'JSESSIONID={session_token}'})
        urlclient = urlopen(request1)
        cppp_page = urlclient.read()
        soup = bs(cppp_page, "html") 

        time.sleep(3)
        article_find = soup.find_all(class_ = 'link2')
        for link_element in article_find:
            link_href = link_element.get('href')
            link_list.add(link_href)
    except Exception as e:
        print("Error in accessing url: {e}")

    try:
        for i in link_list:
            link = 'https://etenders.gov.in'+ i
            request2 = Request(link, headers={'Cookie': f'JSESSIONID={session_token}'})
            
            linkclient = urlopen(request2)
            tender_page = linkclient.read() 
            soup2 = bs(tender_page, "html")
            tender_elements = soup2.find_all('a', {'title': 'View Tender Information'})
            
            # Extracting the href attribute
            for j in tender_elements:
                tender_links = j.get('href')
                tender_link.add(tender_links)
            time.sleep(5)
        print("get_all_links ended successfully")
    except Exception as e:
        print("An error occurred while accessing link:", {link}, {e})
    return tender_link