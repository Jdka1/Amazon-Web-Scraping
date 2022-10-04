import requests
from bs4 import BeautifulSoup
import time
import random


def shorten_name(name):
        all_shortstops = ['-','(',',',':']
        
        shortstops = [
            item for item in all_shortstops if name.find(item) != -1
        ]
        
        if not shortstops:
            return name
        else:
            indxs = [name.index(stop) for stop in shortstops]
            return name[:min(indxs)]   


class Product:
    def __init__(self,price,name):
        self.price = price
        self.name = name
        self.shortname = shorten_name(name)
    
    def print_product(self,shortlong='long'):
        if shortlong.lower() == 'short':
            print(f'${self.price} - {self.shortname}')
        elif shortlong.lower() == 'long':
            print(f'${self.price} - {self.name}')
        
        


def gather_html_pages(query, numpages=1):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'session-id=139-9856532-1745958; session-id-time=2082787201l; i18n-prefs=USD; skin=noskin; ubid-main=134-5936757-7447853; aws_lang=en; aws-target-visitor-id=1664421793462-332564.35_0; aws-target-data=%7B%22support%22%3A%221%22%7D; AMCVS_7742037254C95E840A4C98A6%40AdobeOrg=1; aws-mkto-trk=id%3A112-TZM-766%26token%3A_mch-aws.amazon.com-1664421794050-74096; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C19265%7CMCMID%7C11816054594718087900170928610304657024%7CMCAAMLH-1665026593%7C9%7CMCAAMB-1665026593%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1664428994s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; s_campaign=ps%7Cfce796e8-4ceb-48e0-9767-89f7873fac3d; regStatus=pre-register; s_cc=true; s_eVar60=fce796e8-4ceb-48e0-9767-89f7873fac3d; session-token=D5hyADr61sFfWafNux4PRUTRZh720FKCxBJdNdu6Ya1ttjXNn8Dbe38aMlze4cIF4XMb5cLSECsGCSGSdOu+DlXMlB88EebcsmT5VixOt+6VevlYxyuM6nFGL2RzvVbQce46OZibjGOPbD4lP6L4pAFSzDYGVRBP6WOKhtrgJql1JXRy9JsZQyTaq9AZXgtTXkhAHEKE40j0i/op5z234lyq6cS252S3; csm-hit=adb:adblk_no&t:1664505541444&tb:4QFMEZYH01DY7TQSFT5G+s-5J9G8QQ6W9ATYV19A8JN|1664505541443',
        'device-memory': '8',
        'downlink': '3.8',
        'dpr': '2',
        'ect': '4g',
        'referer': 'https://www.amazon.com/s?k=apple+iphone&crid=G0BB6RXPKKFP&sprefix=applephone%2Caps%2C164&ref=nb_sb_noss_2',
        'rtt': '100',
        'sec-ch-device-memory': '8',
        'sec-ch-dpr': '2',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-ch-viewport-width': '1920',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'viewport-width': '1920'
    }
    
    request_urls = [
        f"https://www.amazon.com/s?i=aps&k={query.replace(' ', '%20')}&page={n}" for n in range(1,numpages+1)
    ]
    
    
    results = []
    
    for url in request_urls:
        results.append(requests.get(url=url, headers=headers).text)
        time.sleep(random.random()*3+1)
        
    return results
    



def search(query, html, explicit=False):
    
    doc = BeautifulSoup(html, 'html.parser')
    output = doc.find_all('div', {'data-component-type': 's-search-result'})
    
    
    product_results = []
    for product in output:
        try:
            product_results.append(Product(
                int(product.find('span',{'class': 'a-price-whole'}).text[:-1]),
                product.find('span',{'class': 'a-size-medium a-color-base a-text-normal'}).text
            ))
        except:
            pass
    
    # Check if all keywords are in product name
    if explicit:
        data = []
        for product in product_results:
            if query.lower() in product.name.lower():
                split_name = product.name.lower().split()
                split_query = query.lower().split()[0]
                if split_query in split_name:
                    prev_indx = split_name.index(split_query) - 1
                    prev_word = split_name[prev_indx]
                    if prev_word != 'for':
                        data.append(product)
                    else:
                        pass
                        # print(f'REMOVING: {product.name}')


    else:
        data = []
        for product in product_results:
            fits = True
            for keyword in query.lower().split():
                if keyword not in product.name.lower():
                    fits = False
                    break
            if fits:
                data.append(product)
        
    
    data = sorted(data, key=lambda product: product.price)
    
    [product.print_product('long') for product in data]
    
    
    

[print('\n') for i in range(10)]


q = 'iphone'


pages = gather_html_pages(q, 1)

for page in pages:
    search(query=q, html=page, explicit=True)

 