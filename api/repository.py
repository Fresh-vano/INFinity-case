from cachetools import TTLCache

class Item:
    def __init__(self, name: str, resource: str, keys: list[str]):
        self.name = name
        self.resource = resource
        self.keys = keys
        
class Repository:
    def __init__(self) -> None:
        self.resources = {}
        self.items = {}
        self.invalidate_cache()

    def invalidate_cache(self):
        self.cache = TTLCache(maxsize=len(self.items), ttl=5)

    def register_resource(self, name: str, resource):
        self.resources[name] = resource

    def add_item(self, item: Item):
        if item.resource not in self.resources:
            raise RuntimeError("unknown resource")
        nres = self.resources[item.resource]
        if nres.validate(item.keys) is False:
            raise RuntimeError("invalid item or resource")
        self.items[item.name] = item
        self.invalidate_cache()

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
    
    def get_items_list(self):
        return list(self.items.keys())
        