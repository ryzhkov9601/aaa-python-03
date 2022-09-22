import json
from typing import Dict


class MyDict(dict):
    """
    A dictionary supporting dot notation.
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in self.items():
            if isinstance(v, dict):
                self[k] = MyDict(v)


class Advert:
    def __init__(self, description: Dict):
        if 'title' not in description:
            raise ValueError('Description of advert missing "title"')
        self.price = description.get('price', 0)
        self._data = MyDict(description)

    def __getattr__(self, item: str):
        return self._data[item]

    def __repr__(self) -> str:
        return f'{self.title} | {self.price} ₽'

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if new_price < 0:
            raise ValueError('Price should be >= 0.')
        self._price = new_price


if __name__ == '__main__':
    # создаем экземпляр класса Advert из JSON
    lesson_str = """{
    "title": "python", "price": 0,
    "location": {
    "address": "город Москва, Лесная, 7",
    "metro_stations": ["Белорусская"]
    }
    }"""
    lesson = json.loads(lesson_str)
    # print(lesson)
    lesson_ad = Advert(lesson)
    # обращаемся к атрибуту location.address
    # print(lesson_ad.price)
    # Out: 'город Москва, Лесная, 7'
    my_dict = Advert(lesson)
    print('Advert representation: ', my_dict)
    print('Advert.price = ', my_dict.price)
    print('Advert.location = ', my_dict.location)
    print('Advert.location.address = ', my_dict.location.address)
