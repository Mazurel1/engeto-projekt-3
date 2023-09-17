# Elections scraper
The project focuses on scraping of electoral data.
### Prerequisities
Install content from requirements.txt.\
pip install -r requirements.txt
### Using the application
After installing the requirements, write the terminal command to start the script.\
python [path to script] [URL] [name of output file]\
It could looks like this: python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4205" new_file.csv
### Code structure
PART 0: Getting and processing input from user.\
PART 1: Getting and processing data from entered URL.\
PART 2: Obtaining and processing data from links that point to individual places.\
PART 3: Taking outputs from part 1 and part 2, process to single output and save to csv file.
### Code description
