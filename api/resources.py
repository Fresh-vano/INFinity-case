from bs4 import BeautifulSoup
import requests
import re

class HTTPResource:
    _headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    }

    def build_concrete_url(self, keys: list[str] = []):
        raise RuntimeError("not implemented method")
    
    def make_resource(self):
        raise RuntimeError("not implemented method")

    def make_resource_list(self):
        raise RuntimeError("not implemented method")
    
    def _load(self, url, handler):
        resp = requests.get(url, headers=HTTPResource._headers)
        if resp.status_code == 200:
            return handler(resp)
        else:
            return None 
        
    def load_resource(self, keys: list[str] = []):
        url = self.build_concrete_url(keys)
        return self._load(url, self.make_resource)
    
    def load_resource_list(self):
        return self._load(self.url_list, self.make_resource_list)
        
    def validate(self, keys: list[str]):
        return self.load_resource(keys) != None
        
class CurrencyMOEXResource(HTTPResource):
    def __init__(self) -> None:
        self.url_list = 'https://iss.moex.com/iss/statistics/engines/futures/markets/indicativerates/securities.json'
        self.url_concrete = 'https://iss.moex.com/iss/statistics/engines/futures/markets/indicativerates/securities/{}/RUB.json'
        super().__init__()

    def build_concrete_url(self, keys: list[str] = []):
        return self.url_concrete.format(keys[0])
    
    def make_resource(self, resp: requests.Response):
        data = resp.json()
        try:
            # Получаем последнюю доступную информацию о курсе
            last_rate_data = data['securities.current']['data'][0]
            # Извлекаем курс из данных
            rate = last_rate_data[3]  # rate находится на 4-й позиции в данных
        except:
            rate = ''

        return str(rate)
    
    def make_resource_list(self, resp: requests.Response):
        data = resp.json()
        lst = []
        try:
            descs = data['securities.list']['data']
            for cr in descs:
                lst.append({"name": cr[0].split('/')[0], "description": cr[1]})
        except:
            pass
        return lst
    
class MetalsRuInvestingResource(HTTPResource):
    def __init__(self) -> None:
        self.url_list = 'https://ru.investing.com/commodities/metals'
        self.url_concrete = 'https://ru.investing.com/commodities/{}-contracts'
        super().__init__()

    def simplify_name(self, name: str):
        return '-'.join([''.join([ch for ch in s if ch not in '$&%#']) for s in re.split('\s+', name.lower())])

    def build_concrete_url(self, keys: list[str] = []):
        return self.url_concrete.format(keys[0])
    
    def make_resource_list(self, resp: requests.Response):
        soup = BeautifulSoup(resp.text, 'html.parser')
        data = soup.find(id="BarchartDataTable").find_all("a")
        return [{'name': self.simplify_name(x.text), 'description': x.attrs['title']} for x in data if x.has_attr('title')]
    
    def make_resource(self, resp: requests.Response):
        soup = BeautifulSoup(resp.text, 'html.parser')
        data = soup.find(id='last_last')
        return data.text