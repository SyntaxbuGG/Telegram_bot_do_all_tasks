# Stack

class Stack:
    def __init__(self):
        self.elements = []

    def push(self, element):
        self.elements.append(element)

    def pop(self):
        if not self.is_empty:
            return self.elements.pop()

    def top(self):
        if not self.is_empty:
            return self.elements[-1]
        return None

    @property
    def is_empty(self):
        return len(self.elements) <= 0

    def __len__(self):
        return len(self.elements)


stack = Stack()


class Item:
    def __init__(self, name, price, qnt):
        self.name = name
        self.price = price
        self.qnt = qnt

    def amount(self):
        return self.price * self.qnt

    def __repr__(self):
        return self.name


class Cart:
    def __init__(self):
        self.items = []

    def __iadd__(self, other):
        self.items.append(other)
        return self


item1 = Item('Apple', 500, 3)
item2 = Item('Limon', 890, 8)
cart = Cart()
cart += item1
cart += item2
print(cart.items)

