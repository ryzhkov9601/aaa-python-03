import json
from typing import Dict
import keyword


def isidentifier(ident: str) -> bool:
    """Determines if string is valid Python identifier."""

    if not isinstance(ident, str):
        raise TypeError("expected str, but got {!r}".format(type(ident)))

    if not ident.isidentifier():
        return False

    if keyword.iskeyword(ident):
        return False

    return True


class ColorizeMixin:
    def colorize(self, text):
        return f'\033[0;{self.repr_color_code};1m' + text + '\033[0;0;0m'


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
        print(isidentifier(item[:-1]))
        if isidentifier(item[:-1]):
            return self._data[item]
        else:
            return self._data[item[:-1]]

    def __repr__(self) -> str:
        return self.colorize(f'{self.title} | {self.price} ₽')

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
                "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
        }
    }"""
    corgi = json.loads(corgi_str)
    corgi_ad = Advert(corgi)
    print('Advert representation: ', corgi_ad)
    print('Advert.price = ', corgi_ad.price)
    print('Advert.class_ = ', corgi_ad.class_)
    print('Advert.location.address = ', corgi_ad.location.address)
