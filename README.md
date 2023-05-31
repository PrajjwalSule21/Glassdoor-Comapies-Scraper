# Glassdoor Companies Scraper
 
This is a Python web scraping project that allows you to extract information about IT companies located in Indore from Glassdoor. The project automates the process of scraping company details such as their name, rating, location, employee size, industry, and reviews from page 1 to the last page.

# Prerequisites

Before running the project, make sure you have the following installed:

-	 Python (version 3.6 or higher)
-	`requests` library
-	`BeautifulSoup` library
-	`pandas` library

# Installation
1.	Clone this repository to your local machine or download the ZIP file.
2.	Install the required libraries by running the following command:
`pip install requests beautifulsoup4 pandas` 

# Usage
1.	Open the glassdoor_companies_scraper.py file.
2.	Modify the min_page_no and max_page_no variables according to the range of pages you want to scrape. By default, the script scrapes from page 1 to page 70.
3.	Run the script using the following command:
`python glassdoor_companies_scraper.py`
4.	The script will scrape the company information from Glassdoor and save each page's data as a separate CSV file in the Companies-csv-files directory.
5.	After scraping all the pages, the script will merge all the CSV files into a single file named CompaniesFinal.csv.

# Credits
This project was developed by Prajjwal Sule.

# License
This project is licensed under the MIT License.

