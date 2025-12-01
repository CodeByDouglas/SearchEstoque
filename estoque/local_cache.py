_ESTOQUE_HASHMAP = None

def get_hashmap():
    global _ESTOQUE_HASHMAP
    return _ESTOQUE_HASHMAP

def set_hashmap(data):
    global _ESTOQUE_HASHMAP
    _ESTOQUE_HASHMAP = data

def invalidate_hashmap():
    global _ESTOQUE_HASHMAP
    _ESTOQUE_HASHMAP = None
