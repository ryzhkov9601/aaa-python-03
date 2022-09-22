import pytest
import json
from Advert import Advert, ColorizeMixin


class TestAdvert:
    iphone = """{
        "title": "iPhone X",
        "price": 100,
        "location": {
            "address": "город Самара, улица Мориса Тореза, 50",
            "metro_stations": ["Спортивная", "Гагаринская"]
        }
    }"""

    corgi = """{
        "title": "Вельш-корги",
        "price": 1000,
        "class": "dogs",
        "location": {
            "address": "сельское поселение Ельдигинское, поселок санатория\
            Тишково, 25"
        }
    }"""

    data_without_title = '{"price": 15}'
    data_without_price = '{"title": "my car"}'
    data_negative_price = '{"title": "house", "price": -10}'

    def custom_parametrize(params, id_params=None):
        return pytest.mark.parametrize(
            'data_dict', params, ids=id_params, indirect=True)

    @pytest.fixture
    def data_dict(self, request):
        return json.loads(request.param)

    @custom_parametrize([iphone, corgi], ['iphone', 'corgi'])
    def test_dot_notation(self, data_dict):
        assert Advert(data_dict).title == data_dict['title']

    @custom_parametrize([iphone, corgi], ['iphone', 'corgi'])
    def test_nested_dot_notation(self, data_dict):
        addr = data_dict['location']['address']
        assert Advert(data_dict).location.address == addr

    @custom_parametrize([data_without_title])
    def test_missing_title(self, data_dict):
        with pytest.raises(ValueError):
            Advert(data_dict)

    @custom_parametrize([data_negative_price])
    def test_negative_price(self, data_dict):
        with pytest.raises(ValueError):
            Advert(data_dict)

    @custom_parametrize([data_without_price])
    def test_default_price(self, data_dict):
        assert Advert(data_dict).price == 0

    testdata = [
        (iphone, '\033[0;33;1miPhone X | 100 ₽\033[0;0;0m'),
        (corgi, '\033[0;33;1mВельш-корги | 1000 ₽\033[0;0;0m'),
    ]

    @pytest.mark.parametrize(
        'data_dict, repr', testdata,
        ids=['iphone', 'corgi'], indirect=['data_dict'])
    def test_repr(self, data_dict, repr):
        assert Advert(data_dict).__repr__() == repr
