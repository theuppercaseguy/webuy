import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import re
import time
# pattern = r'[^\w\s£$€¥₹,.]'
pattern = r'[\x80-\xFF]'

def scrape_items_ebay(website,keyword):
    url = f"https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2332490.m570.l1313&_nkw={keyword}&_sacat=0"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        items = []

        # Find all the relevant elements containing the item information
        category = keyword
        for item in soup.find_all('div', class_='s-item__wrapper'):
            name = item.find('div', class_='s-item__title').text.strip()
            price = item.find('span', class_='s-item__price').text.strip()
            price = re.sub(pattern,"",price)
            img = item.find('div',class_='s-item__image-wrapper image-treatment').img['src']
            url = item.find('a', class_='s-item__link')['href']
            items.append({
                'Name': name,
                'Price': price,
                'Category':category,
                'Description': "description",
                'Tags':category,
                'URL': url,
                'Image_URL':img,
                'website':website,
            })
            print("item collected and saved")

        return items
    else:
        print("Failed to retrieve data")
        return None

def scrape_items_newegg(website,keyword):
    url = f"https://www.newegg.com/p/pl?d={keyword}"
    url = url.replace(" ","+")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    time.sleep(5)
    response = requests.get(url, headers=headers)

    
    print("status",response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        items = []

        category = keyword
        for item in soup.find_all('div', class_='item-cell'):
            name = item.find('a', class_='item-title').text.strip()
            price = item.find('span', class_='price-current-label').text.strip()
            img = item.find('img', class_='checkedimg2 checkedimg')
            url = item.find('a', class_='item-title')['href']
            items.append({
                'Name': name,
                'Price': price,
                'Category': category,
                'Description': "description",
                'Tags': category,
                'URL': url,
                'img': img,
                'website':website
            })
            print("item collected and saved")

        return items
    else:
        print("Failed to retrieve data")
        return None

def save_to_csv(items, filename):
    keys = items[0].keys()
    with open(filename, 'a', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        # dict_writer.writeheader()
        dict_writer.writerows(items)


def main():    
    predefined_categories = ['keyboard', 'mouse', 'monitors', 'graphics card']
    websites = ['eBay','BestBuy']
    
    print("Select a website to search on:")
    for i, site in enumerate(websites, 1):
        print(f"{i}. {site}")

    website_choice = input("Enter your choice: ")
    if(website_choice  not in('1' , '2')):
        website_choice = '1'
    
    website_choice = websites[int(website_choice) - 1]
    
    while True:
        print("Select a category to update, by entering the corresponding number:")
        for i, category in enumerate(predefined_categories, 1):
            print(f"{i}. {category.capitalize()}")

        print(f"{len(predefined_categories) + 1}. Custom")
        
        choice = input("Enter your choice: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(predefined_categories):
                keyword = predefined_categories[choice - 1]
                break
            elif choice == len(predefined_categories) + 1:
                keyword = input("Enter your custom search term, beware this will create a separate category: ")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and", len(predefined_categories) + 1)
        except ValueError:
            print("Invalid input. Please enter a number.")

    if website_choice == 'BestBuy':
        items = scrape_items_newegg(website_choice,keyword)
    elif website_choice == 'eBay':
        items = scrape_items_ebay(website_choice,keyword)[1:]
    else:
        print("Invalid website selected.")

    if items:
        save_to_csv(items,".\\computer_parts\\static\\computer_parts\\cateloge.csv")
        # save_to_csv(items,"cateloge.csv")
        print(f"Data saved to cateloge.csv")
    else:
        print("No items found")

if __name__ == "__main__":
    main()
