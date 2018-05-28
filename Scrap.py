#coding: utf-8

import csv
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

url = "http://www.hotzvim.org.il/%D7%94%D7%A6%D7%98%D7%A8%D7%A4%D7%95%D7%AA-%D7%9C%D7%9E%D7%A0%D7%94%D7%9C%D7%AA/%D7%97%D7%91%D7%A8%D7%95%D7%AA-%D7%91%D7%9E%D7%A0%D7%94%D7%9C%D7%AA/"

def write_to_csv(dataToCSV):
    keys = dataToCSV[0].keys()
    with open('companies.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dataToCSV)

    return dataToCSV

def get_text_from_element(element, selector, rstrip=False, attr_=""):
    try:
        if not attr_:
            text = element.select(selector)[0].text
        else:
            text = element.select(selector)[0].get(attr_)
            if "mailto:" in text:
                text = text[7:]
        
        if rstrip:
            text = text.rstrip()

        return text
    except Exception as e:
        return "N/A"


    
def get_contacts(url):
    
    web_page = requests.get(url)
    return web_page.content

content = get_contacts(url)
content_parsed = BeautifulSoup(content, "html5lib")

companies = []

for company in content_parsed.find_all("div", class_="company-item"):
    # import pdb
    # pdb.set_trace()
    company_information = {
        "title_he": get_text_from_element(company, "h3.company-title"),
        "title_en": get_text_from_element(company, "h4.company-title-en"),
        "address": get_text_from_element(company, "p.company-address", True),
        "tel": get_text_from_element(company, "a.company-phone", True),
        "email": get_text_from_element(company, "a.company-email.company-icon", True, "href"),
        "description": get_text_from_element(company, "p.company-excerpt", True)
    }

    companies.append(company_information)

write_to_csv(companies)