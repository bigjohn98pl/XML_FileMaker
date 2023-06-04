class Block:
    count = 0  # Class variable to keep track of the block count

    def __init__(self, name, shape, params=None):
        self.name = name
        self.number = Block.count + 1
        self.id = f"{self.name}_{self.number}"
        self.shape = shape
        self.params = params or {}
        Block.count += 1

    def add_param(self, key, value):
        self.params[key] = value
        
    def __str__(self) -> str:
        return f"{self.params}"