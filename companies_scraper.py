import requests
from bs4 import BeautifulSoup
import pandas as pd
import glob
import os


def page_authentication(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code < 200 or response.status_code > 299:
        raise Exception('Failed to load the page {}').format(url)
    page_content = response.text
    webpage =  BeautifulSoup(page_content, 'html.parser')
    return webpage


def company_extractor(webpage):
    #extract name of company
    name_class = 'align-items-center mb-xsm'
    comp_name = webpage.find_all('span', {"class":name_class})
    company_name = []
    for tag in comp_name:
        company_name.append(tag.text[:-4])

    # extract starts(rating) of company
    comp_star = webpage.find_all('span', {'class':'pr-xsm ratingsWidget__RatingsWidgetStyles__rating'})
    company_star = []
    for tag in comp_star:
        company_star.append(float(tag.text))

    # extract location of company
    loc_class = 'd-block mt-0 css-56kyx5'
    comp_loc = webpage.find_all('span', {'class':loc_class, 'data-test':"employer-location"})
    company_location = []
    for tag in comp_loc:
        company_location.append(tag.text)

    #extract employee size of company
    comp_size_class = 'd-block mt-0 css-56kyx5'
    comp_size = webpage.find_all('span', {'class':comp_size_class, 'data-test':'employer-size'})
    company_empoyee_size = []
    for tag in comp_size:
        company_empoyee_size.append(tag.text[:-9].strip())

    # extract industry of company
    comp_industry_class = 'd-block mt-0 css-56kyx5'
    comp_industry = webpage.find_all('span', {'class':comp_industry_class, 'data-test':'employer-industry'})
    company_industry = []
    for tag in comp_industry:
        company_industry.append(tag.text)

    # extract review of a company
    comp_review_class = 'mt-xsm mt-md-0'
    comp_review = webpage.find_all('h3', {'class':comp_review_class, 'data-test':'cell-Reviews-count'})
    company_review = []
    for tag in comp_review:
        company_review.append(tag.text)

    # make a dataframe
    company_dict = {
        'Company':company_name,
        'Rating': company_star,
        'Location': company_location,
        'Employee_Size': company_empoyee_size,
        'Industry':company_industry,
        'Review':company_review
    }

    company_df = pd.DataFrame(company_dict)

    return company_df


def csv_maker(dataframe, filename):
    dataframe.to_csv(f"Companies-csv-files\{filename}.csv", index=None)


def csv_merger(path):
    all_files = glob.glob(path + "/*.csv")
    df_lst = []
    for filename in all_files:
        df = pd.read_csv(filename,index_col=None, header=0)
        df_lst.append(df)
    # print(df_lst)
    final_dataframe = pd.concat(df_lst, axis=0, ignore_index=True)
    final_dataframe.to_csv('CompaniesFinal.csv', index=None)

    

if __name__ == "__main__":
    # Automate the whole scrapping from page 1 to page 70
    min_page_no = 1
    max_page_no = 70

    for pg_number in range(min_page_no, max_page_no+1):
        pg_url = f'https://www.glassdoor.co.in/Explore/browse-companies.htm?overall_rating_low=3.5&page={pg_number}&locId=1079&locType=M&locName=Indore&sector=10013&filterType=RATING_OVERALL'
        csv_maker(dataframe=company_extractor(webpage=page_authentication(url=pg_url)), filename = 'page'+str(pg_number))

    # merge all the csv files into one file
    filepath = 'Companies-csv-files/'
    csv_merger(path=filepath)
    
    



