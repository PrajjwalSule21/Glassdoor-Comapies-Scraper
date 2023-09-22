from companies_scraper import page_authentication as Auth
from companies_scraper import company_extractor as Scraper
from companies_scraper import csv_merger as Merger
from companies_scraper import csv_maker as Maker
import warnings
warnings.filterwarnings("ignore")


# Automate the whole scrapping from page 1 to page 70
min_page_no = 1
max_page_no = 70


if __name__ == "__main__":
    for pg_number in range(min_page_no, max_page_no+1):
        pg_url = f'https://www.glassdoor.co.in/Explore/browse-companies.htm?overall_rating_low=3.5&page={pg_number}&locId=1079&locType=M&locName=Indore&sector=10013&filterType=RATING_OVERALL'
        webpage, response = Auth(pg_url) # done authentication and return webpage
        data = Scraper(webpage)  # scrpae the given web page and return a pandas dataframe which contatins all data
        Maker(data, filename = 'page'+str(pg_number)) # make the csv files of the dataframe.

        # csv_maker(dataframe=company_extractor(webpage=page_authentication(url=pg_url)), filename = 'page'+str(pg_number))

    # merge all the csv files into one file
    filepath = 'Companies-csv-files/'
    Merger(path=filepath)
    
