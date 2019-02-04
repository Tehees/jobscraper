# coding: utf-8
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time

URL = "https://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=New+York&start=10"

page = requests.get(URL)

soup = BeautifulSoup(page.text, "html.parser")

def extract_job_title_from_result(soup):
  jobs = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
      jobs.append(a["title"])
  return(jobs)
  
def extract_company_from_result(soup): 
  companies = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    company = div.find_all(name="span", attrs={"class":"company"})
    if len(company) > 0:
      for b in company:
        companies.append(b.text.strip())
    else:
      sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
      for span in sec_try:
        companies.append(span.text.strip())
  return(companies)
 
def extract_location_from_result(soup):
  locations = []
  spans = soup.find_all(name="span", attrs={"class":"location"})
  for span in spans:
    locations.append(span.text)
  return(locations)

output3 = extract_location_from_result(soup)
output2 = extract_company_from_result(soup)
output = extract_job_title_from_result(soup)

combined_dict = dict(zip(output,output2))
print(combined_dict)
print(output3)
