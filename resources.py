import requests
import json

class HTTPResource:
    def build_url(self):
        raise RuntimeError("not implemented method")
    def make_resource(self):
        raise RuntimeError("not implemented method")
    def set_name(self, name):
        self.name = name
    def load_resource(self):
        url = self.build_url()
        resp = requests.get(url)
        if resp.status_code == 200:
            return self.make_resource(resp)
        else:
            return 'Нет данных'
        
class CurrencyMOEXResource(HTTPResource):
    def __init__(self, name) -> None:
        self.prefix = 'https://iss.moex.com/iss/statistics/engines/futures/markets/indicativerates/securities/{}/RUB.json'
        self.name = name
        super().__init__()
    def build_url(self):
        return self.prefix.format(self.name)
    def make_resource(self, resp):
        data = resp.json()
        # Получаем последнюю доступную информацию о курсе
        last_rate_data = data['securities.current']['data'][0]
        # Извлекаем курс из данных
        rate = last_rate_data[3]  # rate находится на 4-й позиции в данных
        return rate