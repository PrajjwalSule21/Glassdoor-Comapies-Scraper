import requests
from bs4 import BeautifulSoup
import pandas as pd
import glob
from urllib.request import urlopen, Request
import os


def page_authentication(url):
    # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Windows Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    header = {'User-Agent': 'Mozilla/5.0'}
    response = Request(url, headers=header)
    page = urlopen(response)
    if page is None:
        raise Exception(f'Failed to load the page {url}')
    webpage =  BeautifulSoup(page, 'html.parser')
    return webpage, response


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
    path = os.getcwd()
    csvdirectory = os.path.join(path, 'Companies-csv-files')
    
    if not os.path.exists('Companies-csv-files'):
        os.mkdir(csvdirectory)

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

    
    



