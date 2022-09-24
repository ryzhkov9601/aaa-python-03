import json
from typing import Dict
import keyword


class ColorizeMixin:
    """
    Mix-in class for colorizing representation.
    """

    def __repr__(self) -> str:
        return self.colorize(f'{self.title} | {self.price} ₽')

    def colorize(self, text):
        color_code = f'\033[0;{self.repr_color_code};1m'
        reset_color_code = '\033[0;0;0m'
        return color_code + text + reset_color_code


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


class Advert(ColorizeMixin):
    repr_color_code = 33

    def __init__(self, description: Dict):
        if 'title' not in description:
            raise ValueError('Description of advert missing "title"')
        self.price = description.get('price', 0)
        self._data = MyDict(description)

    def __getattr__(self, item: str):
        if keyword.iskeyword(item[:-1]) and (item[-1] == '_'):
            return self._data[item[:-1]]
        else:
            return self._data[item]

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if new_price < 0:
            raise ValueError('Price must be >= 0')
        self._price = new_price


if __name__ == '__main__':
    # создаем экземпляр класса Advert из JSON
    corgi_str = """{
        "title": "Вельш-корги",
        "price": 1000,
        "class": "dogs",
        "location": {
            "address":
                "сельское поселение Ельдигинское, поселок санатория Тишково,25"
        }
    }"""
    corgi_dict = json.loads(corgi_str)
    corgi_ad = Advert(corgi_dict)
    print('Advert representation: ', corgi_ad)
    print('Advert.price = ', corgi_ad.price)
    print('Advert.class_ = ', corgi_ad.class_)
    print('Advert.location.address = ', corgi_ad.location.address)
