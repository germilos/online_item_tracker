import json


class Item:
    def __init__(self, url, name, price, available, additional_info):
        self.url = url
        self.name = name
        self.price = price
        self.available = available
        # Some sort of map - similar to object in JS
        self.additional_info = additional_info

    def __repr__(self):
        return f"Name: ({self.name!r}, Price: {self.price!r}, Available: {self.available!r})"

    def __str__(self):
        return f"Name: {self.name}, Price: {self.price}, Available: {self.available}"

    def to_json(self):
        return json.dumps(self, indent=4, default=lambda o: o.__dict__)
