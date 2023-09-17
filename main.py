"""
Elections_Scraper.py: třetí projekt do Engeto Online Python Akademie

autor: Jaroslav Hoferek
email: jaroslav.hoferek@seznam.cz
discord: Jaroslav H. | Mazurel#7763
"""

import requests
from bs4 import BeautifulSoup
import sys
import csv
from collections import defaultdict
from itertools import zip_longest

# PART 0: Get input from user.
def user_input_processing(input) -> str:
    """Get the correct entry from the user."""
    if len(input) != 3:
        print("The correct number of arguments has not been entered.")
        quit()
    elif "https" not in input[1]:
        print("The position of arguments wasn't entered correctly.")
        quit()
    elif input[2].endswith(".csv") != True:
        print("The wrong file format was entered.")
        quit()
    url = input[1]
    file_name = input[2]
    return url, file_name

main_url, fileName = user_input_processing(sys.argv)

# PART 1: Obtain and process data from main page. 

def data_download(url) -> requests.models.Response:
    """Obtain data from website."""
    data_from_url = requests.get(url)
    return data_from_url

main_data = data_download(main_url)
soup = BeautifulSoup(main_data.text, features="html.parser")
id_and_links = soup.find_all("td",{"class": "cislo"})
names_of_units = soup.find_all("td",{"class": "overflow_name"})

def extract_data_from_td(td_data) -> list:
    """
    Processes data from TD to a dictionary 
    that it stores in the list.
    """
    storage_list = []
    for i in td_data:
        td_data_dict = {}
        td_data_dict = i.text
        storage_list.append(td_data_dict)
    return storage_list

id_codes = extract_data_from_td(id_and_links)
place_names = extract_data_from_td(names_of_units)

def get_hyperlinks(id_and_links) -> list:
    """Obtaining links to detail unit page"""
    hyperlinks = []
    links = []
    for link in id_and_links:
        link = link.find('a')['href']
        hyperlinks.append(link)
    for link in hyperlinks:
        first_part_of_link = "https://volby.cz/pls/ps2017nss/"
        full_link = first_part_of_link + link
        links.append(full_link)
    return links

hyperlinks = get_hyperlinks(id_and_links)

def processing_data_to_dict(id_and_links) -> list:
    """
    Processes obtained data into 
    a list of dictionaries.
    """
    index = 0
    storage_list = []
    for i in id_and_links:
        i = {"Place id": id_codes[index], "Place name": place_names[index], "Links": hyperlinks[index]}
        storage_list.append(i)
        index += 1
    return storage_list

main_page_data = processing_data_to_dict(id_and_links)

# PART 2: Obtain and processes data from each place.

def get_general_data_of_the_place(hyperlinks: list) -> list:

    hyperlinks_data = []
    
    for i in hyperlinks:
        data = requests.get(i)
        soup = BeautifulSoup(data.text, "html.parser")
        voters = soup.find("td", headers="sa2")
        issued_envelopes = soup.find("td", headers="sa3")
        submitted_envelopes = soup.find("td", headers="sa5")
        valid_votes = soup.find("td", headers="sa6")
        voters,issued_envelopes,submitted_envelopes,valid_votes = voters.text,issued_envelopes.text,submitted_envelopes.text,valid_votes.text
        dict_part = {"Voters in the list": voters,"Issued envelopes": issued_envelopes, "Submitted envelopes": submitted_envelopes, "Valid votes": valid_votes}
        hyperlinks_data.append(dict_part)
        
    return hyperlinks_data

place_data = get_general_data_of_the_place(hyperlinks)
index= 0
for i in main_page_data:
    i.pop("Links")
    i = i.update(place_data[index])
    index += 1

def political_parties(hyperlinks):
    """
    Obtain names of political parties.
    """
    political_parties = []
    index = 0
    for i in hyperlinks:
        data = requests.get(i)
        soup = BeautifulSoup(data.text, "html.parser")
        political_parties_names = soup.find_all("td", {"class": "overflow_name"})
        for a in political_parties_names:
            a = a.text
            political_parties.append(a)
            index += 1
    return political_parties

def political_parties_results(hyperlinks):
    """
    Obtain political parties results.
    """
    parties_results = []
    for i in hyperlinks:
        for i in hyperlinks:
            data = requests.get(i)
            soup = BeautifulSoup(data.text, "html.parser")
            political_results_a = soup.find_all("td", {"headers": "t1sa2 t1sb3"})
            political_results_b = soup.find_all("td", {"headers": "t2sa2 t2sb3"})
            for a in political_results_a:
                a = a.text
                parties_results.append(a)
            for b in political_results_b:
                b = b.text
                parties_results.append(b)
        return parties_results
    
parties = political_parties(hyperlinks)
results = political_parties_results(hyperlinks)

# PART 3: Connect data to one variable and write to csv file.

data_dict = defaultdict(list)
for parties, results in zip(parties,results):
    data_dict[parties].append(results)

data_list = [dict(zip(data_dict.keys(), v)) for v in zip_longest(*data_dict.values(), fillvalue="")]

for a, b in zip(main_page_data,data_list):
    a.update(b)

def write_data(main_page_data: list, fileName: str) -> str:
    """
    Write data to csv file.
    """
    with open(fileName, mode="w", encoding="utf-8", newline="") as csv_file:
        columns = main_page_data[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(main_page_data)
write_data(main_page_data,fileName)

