# Elections scraper
The project focuses on scraping of electoral data from https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ.
### Prerequisities
Install content from requirements.txt.\
pip install -r requirements.txt
### Using of application
After installing the requirements:\
Step No. 1: Follow this sintax: python [path to script] [URL] [name of output file]\
Step No. 2: Choose an item from the territorial unit, click and use the URL as the first argument.\
Step No. 3: Write name of your input file with ".csv" extension.\
It could looks like this:\
PS E:\Downloads\Scraper> python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4205" new_file.csv\
Final result could looks like this:\
![csvdata](https://github.com/Mazurel1/engeto-projekt-3/assets/137199401/0bf64518-b56c-462c-9690-85020c5bbef3)
### Code structure
PART 0: Getting and processing input from user.\
PART 1: Getting and processing data from entered URL.\
PART 2: Obtaining and processing data from links that point to individual places.\
PART 3: Taking outputs from part 1 and part 2, process to single variable and save to csv file.
### Code description
#### PART 0: Getting and processing input from user
In this section, the user enter the input data. Input data are evaluate according few conditions.
- Command must contain two arguments.
- Arguments are entered in the correct order.
- Output file contain right extension ".csv".
#### PART 1: Getting and processing data from entered URL
In this part is sent GET request to server for data of the page which URL refers to.\
After data parsing, the IDs of places, names of places and liks refer to the detail of the place are selected.\
Variables with IDs, names and hyperlinks are stored to dictionary main_page_data\
(this dictionary will be gradually modified and will serve as a final input for enrollment in CSV).
#### PART 2: Obtaining and processing data from links that point to individual places
This part scrape data from each place which are contains in tables of first link. First are taken data\
from table which contain general data. This data are used for extension of variable "main_page_data",\
and there we get first part of final table.
Next two stem are for obtain data about political parties (name of parties and results), and are stored to two wariables.
These wariables are used in part 3.
#### PART 3: Taking outputs from part 1 and part 2, process to single variable and save to csv file
The first step of this part is to take variables containing political parties and results and create a list of dictionaries\
where the names of the parties are used as keys. The second step is to expand the "main_page_data" by these dictionaries.
The third step writes the final variable "Main_page_data" containing all scratches and sorted data to CSV.
