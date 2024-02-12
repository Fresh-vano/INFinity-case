from cachetools import TTLCache

class Item:
    """
    Вспомогательный класс, содержащий имя нужной нам информации, название модуля ресурса, ответственного за получение этой единиы
    и список ключевых слов, соответствующий предыдущим параметрам.
    """
    def __init__(self, name: str, resource: str, keys: list[str]):
        self.name = name
        self.resource = resource
        self.keys = keys
        
class Repository:
    """
    Фасад для API, который взаимодействует с ресурсами для получения и дополнительной обработки информации.
    """
    def __init__(self) -> None:
        self.resources = {}
        self.items = {}
        self.invalidate_cache()

    """
    Инвалидация кэша
    Кэш необходим для in-memory хранения часто запрашиваемых данных
    """
    def invalidate_cache(self):
        self.cache = TTLCache(maxsize=len(self.items), ttl=5)

    """
    Зарегистрировать ресурс
    """
    def register_resource(self, name: str, resource):
        self.resources[name] = resource

    """
    Добавить инструмент
    """
    def add_item(self, item: Item):
        if item.resource not in self.resources:
            raise RuntimeError("unknown resource")
        nres = self.resources[item.resource]
        if nres.validate(item.keys) is False:
            raise RuntimeError("invalid item or resource")
        self.items[item.name] = item
        self.invalidate_cache()

    """
    Получить текущую цену в относительных единицах для конкретного инструмента
    """
    def get_value_by_item(self, name: str):
        if name not in self.items:
            raise RuntimeError("unknown item")
        cached = self.cache.get(name, None)
        if cached != None:
            self.cache.update({name: cached})
            return cached
        item = self.items[name]
        resource = self.resources[item.resource]
        val = resource.load_resource(item.keys)
        self.cache[name] = val
        return val 
    
    """
    Получить список доступных инструментов
    """
    def get_items_list(self):
        return list(self.items.keys())
        