import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    }

games_sale = []

def collect_data(next_page):
    s = requests.Session()
    url = f'https://www.gamemania.com.ua/playstation-4/igry/?page={next_page}'
    r = s.get(url=url, headers=headers) 
    src = r.text
    soup = BeautifulSoup(src, "lxml")
    
    #Finding out links for pages

    all_links = soup.find_all('form', class_='flexdiscount-product-form')
    if len(all_links) == 0:

            return True

    for link in all_links:
        
        try:

            sale_block = link.find('div', class_="badge discount").text.replace('%', '').lstrip('-')
            name = link.find('div', class_ = 'name').text.replace('...', '').strip()
            price = link.find('div', class_ = 'price').find('span').text.replace(' ', '').replace('грн.', '')
            print(sale_block, name, price)
            print("___________________________"*3)

            if sale_block is not None:
                games_sale.append(
                {
                    'Name': name,
                    'Sale_amount': sale_block,
                    'Price': price
                }
            )
            
        except:
            pass

def upload():

    s = requests.Session()
    url = f'https://www.gamemania.com.ua/playstation-4/igry/?page=1'
    r = s.get(url=url, headers=headers) 
    src = r.text
    soup = BeautifulSoup(src, "lxml")
    stop = soup.find('div', id = 'product-list').text
    i = 1
    while True:
        go = collect_data(i)
        i+=1

        if go:
            break
        
    with open('sale.json', 'w') as f:
        json.dump(games_sale, f)
    print(games_sale)

    print(f'There are {len(games_sale)} games on sale')

def takeSecond(elem):

    return elem.get('Price')


def sort():
    sorted_data = []

    input_price = int(input('Вывести все игры по скидке с ценой меньше (грн): '))

    with open('sale.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    for val in json_data:

        if int(val['Price']) < input_price:
            sorted_data.append(val)
             
    sorted_data.sort(key=takeSecond)

    df = pd.DataFrame(sorted_data).reindex(columns=['Name','Sale_amount','Price'])
    print(df)

def main():

    upload()

    sort()  
        

if __name__ == "__main__":
    main()