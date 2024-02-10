from bs4 import BeautifulSoup
import requests


class HTTPResource:
    def build_url(self):
        raise RuntimeError("not implemented method")
    
    def make_resource(self):
        raise RuntimeError("not implemented method")
    
    def set_name(self, name: list[str]):
        self.name = name

    def load_resource(self):
        url = self.build_url()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        }
        resp = requests.get(url, headers=headers)
        print(resp.status_code)
        if resp.status_code == 200:
            return self.make_resource(resp)
        else:
            return None
        
class CurrencyMOEXResource(HTTPResource):
    def __init__(self, name: list[str]) -> None:
        self.prefix = 'https://iss.moex.com/iss/statistics/engines/futures/markets/indicativerates/securities/{}/RUB.json'
        self.name = name
        super().__init__()

    def build_url(self):
        return self.prefix.format(self.name)
    
    def make_resource(self, resp: requests.Response):
        data = resp.json()
        # Получаем последнюю доступную информацию о курсе
        last_rate_data = data['securities.current']['data'][0]
        # Извлекаем курс из данных
        rate = last_rate_data[3]  # rate находится на 4-й позиции в данных
        return rate
    
class MetalsLMEResource(HTTPResource):
    def __init__(self, name: list[str]) -> None:
        self.prefix = 'https://www.lme.com/Metals/{}/{}'
        self.name = name
        super().__init__()

    def build_url(self):
        return self.prefix.format(self.name[0], self.name[1])
    
    def make_resource(self, resp: requests.Response):
        soup = BeautifulSoup(resp.text, 'html.parser')
        data = soup.find(class_='hero-metal-data__number')
        return data
    
class MetalsRuInvestingResource(HTTPResource):
    def __init__(self, name: list[str]) -> None:
        self.prefix = 'https://ru.investing.com/commodities/{}-contracts'
        self.name = name
        super().__init__()

    def build_url(self):
        return self.prefix.format(self.name[0])
    
    def make_resource(self, resp: requests.Response):
        soup = BeautifulSoup(resp.text, 'html.parser')
        data = soup.find(id='last_last')
        return data.text