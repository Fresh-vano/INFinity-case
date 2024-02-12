from cachetools import TTLCache

class Item:
    def __init__(self, category: str, resource: str):
        self.category = category
        self.resource = resource
        
class Repository:
    def __init__(self) -> None:
        self.resources = {}
        self.items = {}
        self.size = 0
        self.invalidate_cache()

    @staticmethod
    def _build_cache_uri(category: str, keys: list[str]):
        return category + "/".join(keys)
    
    def invalidate_cache(self):
        self.cache = TTLCache(maxsize=self.size, ttl=5)

    def register_resource(self, name: str, resource):
        self.resources[name] = resource

    def add_item(self, item: Item):
        if item.resource not in self.resources:
            raise RuntimeError("unknown resource")
        nres = self.resources[item.resource]
        self.items[item.category] = item
        self.size += len(nres.load_resource_list())
        self.invalidate_cache()

    def get_categories_list(self):
        return list(self.items.keys())

    def get_category_content(self, category: str):
        if category not in self.items:
            raise RuntimeError("unknown category")
        item = self.items[category]
        resource = self.resources[item.resource]
        return resource.load_resource_list()
        
    def get_value_by_params(self, category: str, keys: list[str]):
        if category not in self.items:
            raise RuntimeError("unknown category")
        uri = Repository._build_cache_uri(category, keys)
        cached = self.cache.get(uri, None)
        if cached != None:
            self.cache.update({uri: cached})
            return cached
        item = self.items[category]
        resource = self.resources[item.resource]
        val = resource.load_resource(keys)
        self.cache[uri] = val
        return val