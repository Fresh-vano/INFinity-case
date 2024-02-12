from bs4 import BeautifulSoup
import requests

class HTTPResource:
    """
    Базовый класс для всех ресурсов - тех инструмент, с которыми взаимодействует приложение для получения данных.
    Изначально предусматривается, что ресурс имеет некоторый HTTP-шаблон, который при подстановке необходимых ключевых слов
    преобразуется в URI нужного нам ресурса.
    Подобная конструкция в перспективе позволит очень гибко управлять системой, ориентированной на работу с большим множеством ресурсов.
    """
    def build_url(self, keys: list[str] = []):
        raise RuntimeError("not implemented method")
    
    def make_resource(self):
        raise RuntimeError("not implemented method")

    def load_resource(self, keys: list[str] = []):
        url = self.build_url(keys)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        }
        print(url)
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            return self.make_resource(resp)
        else:
            return None
    
    def validate(self, keys: list[str]):
        return self.load_resource(keys) != None
        
class CurrencyMOEXResource(HTTPResource):
    """
    Ресурс для работы c валютой на Московской бирже.
    """
    def __init__(self) -> None:
        self.prefix = 'https://iss.moex.com/iss/statistics/engines/futures/markets/indicativerates/securities/{}/RUB.json'
        super().__init__()

    def build_url(self, keys: list[str] = []):
        return self.prefix.format(keys[0])
    
    def make_resource(self, resp: requests.Response):
        data = resp.json()
        try:
            # Получаем последнюю доступную информацию о курсе
            last_rate_data = data['securities.current']['data'][0]
            # Извлекаем курс из данных
            rate = last_rate_data[3]  # rate находится на 4-й позиции в данных
        except:
            rate = ''

        return rate
    
class MetalsRuInvestingResource(HTTPResource):
    """
    Ресурс для описания цены металлов с сайта ru.investing.
    """
    def __init__(self) -> None:
        self.prefix = 'https://ru.investing.com/commodities/{}-contracts'
        super().__init__()

    def build_url(self, keys: list[str] = []):
        return self.prefix.format(keys[0])
    
    def make_resource(self, resp: requests.Response):
        soup = BeautifulSoup(resp.text, 'html.parser')
        data = soup.find(id='last_last')
        return data.text