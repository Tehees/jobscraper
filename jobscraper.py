# coding: utf-8
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time

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

def extract_salary_from_result(soup): 
  salaries = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    try:
      salaries.append(div.find("nobr").text)
    except:
      try:
        div_two = div.find(name="div", attrs={"class":"sjcl"})
        div_three = div_two.find("div")
        salaries.append(div_three.text.strip())
      except:
        salaries.append("Nothing_found")
  return(salaries)

def extract_summary_from_result(soup): 
  summaries = []
  spans = soup.findAll("span", attrs={"class": "summary"})
  for span in spans:
    summaries.append(span.text.strip())
  return(summaries)


def find_all_results():

  max_results_per_city = 100
  #city_set = ["New+York","Chicago","San+Francisco", "Austin", "Seattle", "Los+Angeles", "Philadelphia", "Atlanta", "Dallas", "Pittsburgh", "Portland", "Phoenix", "Denver", "Houston", "Miami", "Washington+DC", "Boulder"]
  city_set = ["New York","Toronto", "San Francisco"]
  types_of_jobs = ["Software Engineer", "Bank", "Consulting"]
  columns = ["city", "job_title", "company_name", "location", "summary", "salary"]

  for city in city_set:
    for start in range(0, max_results_per_city):
      page = requests.get("http://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=" + str(city) + "&start=" + str(start))
      #time.sleep(0.05)  #ensuring at least 1 second between page grabs
      soup = BeautifulSoup(page.text, "html.parser")
      
      location_results = extract_location_from_result(soup)
      company_results = extract_company_from_result(soup)
      job_title_results = extract_job_title_from_result(soup)

      job_info = list(zip(location_results, company_results))
    
    
  job_results = dict(zip(job_title_results,job_info))
  print(job_results)

find_all_results()
#output3 = extract_location_from_result(soup)
#output2 = extract_company_from_result(soup)
#output = extract_job_title_from_result(soup)

##combined_dict = dict(zip(output,output2))
#print(combined_dict)
#print(output3)
