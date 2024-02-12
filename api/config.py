from repository import Item, Repository
from resources import *
import json
import platform

CONFIG_PATH = "E:\\INFinity-case\\api\\config.json"

def init_repo():
    global repo
    repo = Repository()
    repo.register_resource('moex-currency',   CurrencyMOEXResource())
    repo.register_resource('ruinvest-metals', MetalsRuInvestingResource())
    with open(CONFIG_PATH) as cfg:
        items = json.load(cfg)
        for item in items:
            repo.add_item(Item(item["name"], item["resource"], item["keys"]))

def handle_sighub():
    init_repo()

# Инициализация репозитория
repo = Repository()
init_repo()

if platform.system() == 'Linux':
    import signal

    # Обновить конфигурацию при сигнале SIGHUB к процессу приложения
    signal.signal(signalnum=signal.SIGTERM, handler=handle_sighub)
