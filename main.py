import os
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import csv
import logging
import string
from datetime import datetime
import time
import requests
import helper_function 
from get_links import get_all_links
from scraping_page import scraping_page
import pandas as pd

url = 'https://etenders.gov.in/eprocure/app?page=FrontEndTendersByOrganisation&service=page'
session_token = helper_function.extract_jsessionid(url)

tender_link=get_all_links(url, session_token)
data_list=scraping_page(tender_link, session_token)
print(len(data_list))
df=pd.DataFrame.from_records(data_list)

df.to_csv('finaldata.csv')
print("saving_data in csv successful.") 