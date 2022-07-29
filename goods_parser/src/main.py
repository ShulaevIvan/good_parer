import requests
from bs4 import BeautifulSoup
from tqdm.auto import trange
from  pprint import pprint



class CitilinkParser():

    def __init__(self):
        self.price_filter  = 40000
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
 
        self.urls = {
            '-n':  'https://www.citilink.ru/catalog/noutbuki/',
            '-c':  'https://www.citilink.ru/catalog/kompyutery/',
            '-mo': 'https://www.citilink.ru/catalog/monitory/',
            '-k':  'https://www.citilink.ru/catalog/klaviatury/',
            '-m':  'https://www.citilink.ru/catalog/myshi/',
            '-km': 'https://www.citilink.ru/catalog/komplekty-klaviatura-mysh/',
            '-b':  'https://www.citilink.ru/catalog/bloki-pitaniya/',
            '-s':  'https://www.citilink.ru/catalog/servernye-platformy/',
            '-r':  'https://www.citilink.ru/catalog/wi-fi-routery-marshrutizatory/',
            '-t':  'https://www.citilink.ru/catalog/tochki-dostupa/',
            '-cm': 'https://www.citilink.ru/catalog/kommutatory/',
            'cc':  'https://www.citilink.ru/catalog/sistemy-ohlazhdeniya-processora/',
            'cp':  'https://www.citilink.ru/catalog/sistemy-ohlazhdeniya-kompyutera/',
            '-pr': 'https://www.citilink.ru/catalog/processory/',
            '-mb': 'https://www.citilink.ru/catalog/materinskie-platy/',
            '-dr': 'https://www.citilink.ru/catalog/moduli-pamyati/',
            '-v':  'https://www.citilink.ru/catalog/videokarty/',
            '-bp': 'https://www.citilink.ru/catalog/bloki-pitaniya/',
            '-hd': 'https://www.citilink.ru/catalog/zhestkie-diski/',
            '-ud': 'https://www.citilink.ru/catalog/vneshnie-zhestkie-diski/',
            '-bl': 'https://www.citilink.ru/catalog/korpusa/',
            '-tv': 'https://www.citilink.ru/catalog/televizory/'
        }

        self.result_obj =  dict()
        self.result_file = 'result.txt'



    def get_content(self, key:str, pages:int=1):

        self.url = ''
        self.user_key = key

        for k, v in self.urls.items():
            if k == self.user_key:
                url = self.urls[k]

        self.pages = pages
        tumbler = True

        for num in trange(1, pages+1):
            r = requests.get(url+f'?p={num}', headers=self.headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            catalog = soup.find_all('div', class_='ProductCardVerticalLayout')

            if catalog == []:
                catalog = soup.find_all('div', class_='product_data__gtm-js')
                tumbler  = False

            for item in catalog:
                
                if tumbler:
                    good = item.find('a', class_='ProductCardVertical__name').get('title')
                    price_str = item.find('span', class_='ProductCardVerticalPrice__price-current_current-price')
    
                else:
                    good = item.find('a', class_='ProductCardHorizontal__title').get('title')
                    price_str = item.find('span', class_='ProductCardHorizontal__price_current-price')

                if price_str == None:
                    continue
                else:
                    price = ''.join(price_str.text.split())
        
                self.result_obj[good] = price

    def write_content(self):
        with open(self.result_file, 'r+') as f:
            for item, price in self.result_obj.items():
                if int(price) > self.price_filter:
                    continue
                else:
                    line = f'{item} : Цена {price} рублей'
                    f.write(f'{line}\n')



if __name__ == '__main__':

    while True:
        print(
        """
            start parser

            Команды для поиска:

            -n  ноутбуки
            -c  компьютеры
            -mo  мониторы
            -k  клавиатуры
            -m  мыши
            -km комплекты клавиатура + мышь
            -b  системные блоки
            -s  серверные платформы
            -r  роутеры
            -t  точки доступа
            -com коммутаторы
            -pr  процессоры
            -mb материнские платы
            -ddr оперативная память
            -v видеокарты
            -bp блоки питания
            -hdd жесткие диски
            -uhdd usb жесткие диски
            -bl корпуса
            -tv телевизоры
        """
        )
        print('Ожидание ввода:')
        ans_key = input()
                
        parser = CitilinkParser()
        parser.get_content(ans_key)
        parser.write_content()

   




        
        


 