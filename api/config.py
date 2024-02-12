from repository import Item, Repository
from resources import *
import json
import platform

CONFIG_PATH = './config.json'

def init_repo():
    global repo
    repo = Repository()
    repo.register_resource('moex-currency',   CurrencyMOEXResource())
    repo.register_resource('ruinvest-metals', MetalsRuInvestingResource())
    with open(CONFIG_PATH) as cfg:
        categories = json.load(cfg)
        for ctg in categories:
            repo.add_item(Item(ctg["category"], ctg["resource"]))

def handle_sighub():
    init_repo()

# Инициализация репозитория
repo = Repository()
init_repo()

if platform.system() == 'Linux':
    import signal

    # Обновить конфигурацию при сигнале SIGHUB к процессу приложения
    signal.signal(signalnum=signal.SIGTERM, handler=handle_sighub)
