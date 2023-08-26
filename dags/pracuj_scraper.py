from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import re
from datetime import date


# Function to extract Job Title
def get_job_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("h1")
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Function to extract Employer Name
def get_employer(soup):

    try:
        # Outer Tag Object
        employer = soup.find("h2")
        
        # Inner NavigatableString Object
        employer_value = employer.contents[0]

        # Title as a string value
        employer_string = employer_value.strip()

    except AttributeError:
        employer_string = ""

    return employer_string

# Function to extract Workplace
def get_workplace(soup):

    try:
        workplace_value = soup.find("div", attrs= {'data-scroll-id':"workplaces-wp"}).contents[1].find_all('p')
        #workplace_value = soup.find("div", class_ = "offer-viewUIYWmu").text

        # Workplace as a string value
        workplace_string = str(workplace_value).split('>')[1].split('<')[0]

    except:
        try:
            workplace_value = soup.find("div", attrs= {'data-scroll-id':"workplaces"}).contents[1].find_all('p')
            #workplace_value = soup.find("div", class_ = "offer-viewUIYWmu").text

            # Workplace as a string value
            workplace_string = str(workplace_value).split('>')[1].split('<')[0]
        except:
            try:
                workplace_value = soup.find("div", attrs= {'data-scroll-id':"workplaces-wp"}).contents[1].find_all('a')
                #workplace_value = soup.find("div", class_ = "offer-viewUIYWmu").text

                # Workplace as a string value
                workplace_string = str(workplace_value).split('>')[1].split('<')[0] 
            except:
                try:
                    workplace_value = soup.find("div", attrs= {'data-scroll-id':"workplaces"}).contents[1].find_all('a')
                    #workplace_value = soup.find("div", class_ = "offer-viewUIYWmu").text

                    # Workplace as a string value
                    workplace_string = str(workplace_value).split('>')[1].split('<')[0] 
                except:    
                    workplace_string = ""
    #except:    
        #workplace_string = ""

    return workplace_string

# Function to extract Job Responsibilities
def get_responsibilities(soup):

    try:
        responsibilities_list = soup.find("div", attrs= {'data-scroll-id':"responsibilities-1"}).contents[1].find_all('p')
        
        responsibilities_string = ''
        for element in responsibilities_list:
            responsibilities_string += '\n- '+element.text
    
    except:
        responsibilities_string = ''

    return responsibilities_string

# Function to extract Job Requirements
def get_requirements(soup):

    try:
        requirements_list = soup.find("div", attrs= {'data-scroll-id':"requirements-1"}).contents[1].find_all('p')
        
        requirements_string = ''
        for element in requirements_list:
            requirements_string += '\n- '+element.text
    
    except:
        responsibilities_string = ''

    return requirements_string

# Function to extract Job Requirements (optional)
def get_optional(soup):

    try:
        optional_list = soup.find("div", attrs= {'data-scroll-id':"requirements-1"}).contents[2].find_all('p')
        
        optional_string = ''
        for element in optional_list:
            optional_string += '\n- '+element.text
    
    except:
        optional_string = ''

    return optional_string



# Function to extract Expiration Date
def get_expiration(soup):
    try:
        expiration = soup.find("div", attrs= {'data-scroll-id':"publication-dates"}).contents[-1].text
        expiration_date = expiration.split(':')[-1].strip()

    except:
        expiration_date = ""

    return expiration_date



def scrape():
    # user agent 
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0', 
                'Accept-Language': 'en-US, en;q=0.5'})

    # The webpage URL, query for: data warehouse developer, Kraków, 30km area, mid, order by date desc
    URL = "https://www.pracuj.pl/praca/data%20warehouse%20developer;kw/krakow;wp?rd=30&et=4&sc=0"

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Fetch all links to job offers
    links = soup.find_all("a", attrs={'listing_n194fgoq'})

    # Store the links
    links_list = []

    # Loop for extracting links from ResultSet list
    for link in links:
            links_list.append(link.get('href'))
    
    #Remove duplicates
    links_list = list(dict.fromkeys(links_list))
    
    #Fitler the list
    pattern = ".*/praca/.*"
    filtered_links_list = [x for x in links_list if re.match(pattern, x)]


    d = {"current_date":[], "job_title":[], "employer":[], "workplace":[], "responsibilities":[],"requirements":[],"optional_req":[],"expiration_date":[]}
    
    # Loop for extracting details from each offer
    for link in filtered_links_list:
        new_webpage = requests.get(link, headers=HEADERS)

        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        d['current_date'].append(date.today())
        d['job_title'].append(get_job_title(new_soup))
        d['employer'].append(get_employer(new_soup))
        d['workplace'].append(get_workplace(new_soup))
        d['responsibilities'].append(get_responsibilities(new_soup))
        d['requirements'].append(get_requirements(new_soup))
        d['optional_req'].append(get_optional(new_soup))
        d['expiration_date'].append(get_expiration(new_soup))
        
        #Minimizing the risk of blockage
        time.sleep(2)
        
    df=pd.DataFrame.from_dict(d)
    df.to_csv('/opt/airflow/dags/out.csv', index=False)
        
            

