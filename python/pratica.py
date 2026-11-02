class list:
    def __init__(self):
        self.items = []

    def append(self, item):
        self.items.append(item)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]