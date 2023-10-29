import os
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import csv
import logging
import string
from datetime import datetime
import time
import requests
import pandas as pd

def scraping_page(tender_link,session_token):
    #get tender link
    data_list=[]
    for k in tender_link:
        try:
            print("Iteration of tender_link started successfully")
            link2 = 'https://etenders.gov.in'+ k
            request2 = Request(link2, headers={'Cookie': f'JSESSIONID={session_token}'})
            link2client = urlopen(request2)
            tender_details = link2client.read() #reading the html page
            soup3 = bs(tender_details, "html")
        except Exception as e:
            print("An error occured in link2: ",link2, e)          
        # For original id
        try:
            td_caption_elements = soup3.find_all('td', class_='td_caption')
            # Tender ID
            for td in td_caption_elements:
                if "Tender ID" in td.get_text():
                    original_id = td.find_next('td').get_text(strip=True)
        except Exception as e:
            original_id = "NaN"
        # For  Title
        try:
            title=soup3.find('td',class_='td_caption',string='Title').find_next('td').get_text(strip=True)
        except Exception as e:
                title = "NaN"
        # For Work Description same value
        try:
            work_description = soup3.find('td', class_='td_caption', string='Work Description').find_next('td').get_text(strip=True)
        except Exception as e:
            work_description = "NaN"
        # For Tender Value
        try:
            tender_value = soup3.find('td', class_='td_caption', string='Tender Value in ₹ ').find_next('td').get_text(strip=True)
            if tender_value != 'NA':
                budget = float(tender_value.replace(',', '')) // 83.15
            else:
                budget = tender_value
        except Exception as e:
            budget = "NaN"
        # For product_Category
        try:
            product_category = soup3.find('td', class_='td_caption', string='Product Category').find_next('td').get_text(strip=True)
        except Exception as e:
            product_category = "NaN"
        # For Sub category
        try:
            subcategory = soup3.find('td', class_='td_caption', string='Sub category').find_next('td').get_text(strip=True)
        except Exception as e:
            subcategory = "NaN"
        # For contract Type
        try:
            contract_type = soup3.find('td', class_='td_caption', string='Contract Type').find_next('td').get_text(strip=True)
            if contract_type == 'Tender':
                P_or_T = "T"
            else:
                P_or_T = "P"
        except Exception as e:
            contract_type = "NaN"   
        # For Location            
        try:
            location = soup3.find('td', class_='td_caption', string='Location').find_next('td').get_text(strip=True)
        except Exception as e:
            location = "NaN"
        # For Published Date
        try:
            tables = soup3.find_all('table', {'class': 'tablebg'})
            target_table = None
        
            for table in tables:
                if 'Published Date' in table.get_text():
                    target_table = table
                    break
        
            if target_table:
                td_elements = target_table.find_all('td')
                date_dict = {}
                current_caption = None
                for td_element in td_elements:
                    bold_tag = td_element.find('b')
                    if bold_tag:
                        current_caption = bold_tag.get_text(strip=True)
                    else:
                        if current_caption:
                            date = td_element.get_text(strip=True)
                            if date != 'NA':
                                date1 = datetime.strptime(date, '%d-%b-%Y %I:%M %p')
                                formatted_date = date1.strftime('%Y-%m-%d %H:%M:%S')
                                date_dict[current_caption.lower()] = formatted_date
                            else:
                                date_dict[current_caption.lower()] = date
                time_stamps = date_dict
        except Exception as e:
            time_stamps = {}
        # Dates
        try:
            published_date = date_dict.get('published date', 'NA')
            bid_opening_date = date_dict.get('bid opening date', 'NA')
            clarification_start_date = date_dict.get('clarification start date', 'NA')
            clarification_end_date = date_dict.get('clarification end date', 'NA')
            bid_submission_start_date = date_dict.get('bid submission start date', 'NA')
            bid_submission_end_date = date_dict.get('bid submission end date', 'NA')
        except Exception as e:
            published_date={}
            bid_opening_date={}
            clarification_start_date={}
            clarification_end_date={}
            bid_submission_start_date={}
            bid_submission_end_date={}
        # For Sale Start Date
        try:
            min_date = date_dict.get('document download / sale start date', 'NA')
            max_date = date_dict.get('document download / sale end date', 'NA')
            timestamp_range = {'min': min_date, 'max': max_date}
        except Exception as e:
            timestamp_range = {}
        #for Document URLs
        try:
            document_urls = []
            anchor_tag = soup3.find('a', {'id': 'docDownoad'})
            if anchor_tag:
                href_link1 = anchor_tag.get('href')
                document_urls.append('https://etenders.gov.in'+href_link1)
            blue_links = soup3.find_all('a', class_='blue_link')
            for link in blue_links:
                href_link2 = link.get('href')
                document_urls.append('https://etenders.gov.in'+href_link2)
        except Exception as e:
            document_urls = []  
        data_format = {}
        data_format["original_id"]= original_id
        data_format["project_or_tender"]= P_or_T
        data_format["name"]= title
        data_format["description"]= work_description
        data_format["source"]= "etenders.gov.in"
        data_format["status"]= "Proposed"
        data_format["identified_status"]= "Proposed"
        data_format["budget"]= budget
        data_format["url"]= link2
        data_format["document_urls"]= document_urls
        data_format["sector"]= product_category
        data_format["subsector"]= subcategory
        data_format["identified_sector"]= product_category
        data_format["identified_subsector"]= subcategory
        data_format["identified_sector_subsector_tuple"]= (product_category, subcategory)
        data_format["country_name"]= "India"
        data_format["country_code"]= "IND"
        data_format["region_name"]= "South Asia"
        data_format["region_code"]= "SAS"
        data_format["timestamps"]= time_stamps
        data_format["published_date"]=published_date
        data_format["bid_opening_date"]=bid_opening_date
        data_format["clarification_start_date"]=clarification_start_date
        data_format["clarification_end_date"]=clarification_end_date
        data_format["bid_submission_start_date"]=bid_submission_start_date
        data_format["bid_submission_end_date"]=bid_submission_end_date
        data_format["timestamp_range"]= timestamp_range
        
        # Appending the data to the data_list
        data_list.append(data_format)
    print("Scraping_page was successfull")
    return data_list
    
   