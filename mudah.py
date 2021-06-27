import requests
import pandas as pd 
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import time 
import datetime

#set amount of page to scrap, edit number before +1 sign
page_key = [*range(1, 3+1, 1)]
print(page_key)

def download_dataset():

    #create list for each variable
    date = []
    area = []
    title = []
    type = []
    bedroom = []
    size = []
    price = []

    for x in page_key:
        key = x
        link = "https://www.mudah.my/list?category=2020&fs=1&lst=0&o={}&so=1&st=s&w=108".format(x)
        
        print("Processing page " + str(key))
        #error exception handling, skip page with no data
        try:
            response = requests.get(link)
            if response.status_code == 404:
                continue
        except:
            pass

        #get each page data
        page = requests.get(link)
        #set program to wait for page to load completely
        time.sleep(30)
        soup = BeautifulSoup(page.text, 'html.parser')

        #get number of rows
        contentTable = soup.find('div', { "class" : "sc-gZMcBi eNtCZJ"})
        rows = contentTable.find_all('div', { "class" : "sc-gxMtzJ daQtBi"})
        number_of_rows = len(rows)

        #set row range to max data in a page
        row_key = [*range(1, number_of_rows, 1)]

        #loop to get each row data
        for y in row_key:
            date1 = contentTable.find_all('span', { "class" : "sc-cmTdod kJycFC"})
            date2 = date1[y].get_text()
            date.append(date2)

            area1 = contentTable.find_all('span', { "class" : "sc-btzYZH cExPek"})
            area2 = area1[y].get_text()
            area.append(area2)

            title1 = contentTable.find_all('a', { "class" : "sc-kIPQKe cQMfNT"})
            title2 = title1[y].get_text()
            title.append(title2)

            type1 = contentTable.find_all('div', { "title" : "Category"})
            type2 = type1[y].get_text()
            type.append(type2)

            bedroom1 = contentTable.find_all('div', { "class" : "sc-eTuwsz fcPuPg"})
            bedroom2 = bedroom1[y].get_text()
            bedroom.append(bedroom2)

            size1 = contentTable.find_all('div', { "title" : "Size"})
            size2 = size1[y].get_text()
            size.append(size2)

            price1 = contentTable.find_all('div', { "class" : "sc-RefOD fjuYGU"})
            price2 = price1[y].get_text()
            price.append(price2)

            mudah_data = pd.DataFrame({

                "Date" : date,
                "Area" : area,
                "Title" : title,
                "Type" : type,
                "Bedroom" : bedroom,
                "Size" : size,
                "Price" : price
            })
    return mudah_data

def cleaning_data(mudah_data):
    #set date to standardized date
    current_date = datetime.datetime.today().strftime ('%d-%b-%Y')
    mudah_data["Date"] = mudah_data["Date"].replace('Today', current_date, regex=True)
    print(mudah_data)
    #output to csv
    mudah_data.to_csv(r'mudah_output.csv', encoding='utf-8-sig', index=False)


#Run script
def main():

    print("Takes around 2 minutes to let website to load properly for scraping")
    mudah_data = download_dataset()
    cleaning_data(mudah_data)
    print("Finished")

if __name__ == "__main__":
    main()