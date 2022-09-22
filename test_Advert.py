import pytest
import json
from Advert import Advert


class Test_Advert:
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

    @pytest.fixture
    def data_dict(self, request):
        return json.loads(request.param)

    @pytest.mark.parametrize(
        'data_dict', [iphone, corgi],
        ids=['iphone', 'corgi'], indirect=True)
    def test_dot_notation(self, data_dict):
        assert Advert(data_dict).title == data_dict['title']

    @pytest.mark.parametrize(
        'data_dict', [iphone, corgi],
        ids=['iphone', 'corgi'], indirect=True)
    def test_nested_dot_notation(self, data_dict):
        addr = data_dict['location']['address']
        assert Advert(data_dict).location.address == addr

    @pytest.mark.parametrize('data_dict', [data_without_title], indirect=True)
    def test_missing_title(self, data_dict):
        with pytest.raises(ValueError):
            Advert(data_dict)

    @pytest.mark.parametrize('data_dict', [data_negative_price], indirect=True)
    def test_negative_price(self, data_dict):
        with pytest.raises(ValueError):
            Advert(data_dict)

    @pytest.mark.parametrize('data_dict', [data_without_price], indirect=True)
    def test_default_price(self, data_dict):
        assert Advert(data_dict).price == 0

    @pytest.mark.parametrize(
        'data_dict, repr',
        [(iphone, 'iPhone X | 100 ₽'), (corgi, 'Вельш-корги | 1000 ₽')],
        ids=['iphone', 'corgi'], indirect=['data_dict'])
    def test_repr(self, data_dict, repr):
        assert Advert(data_dict).__repr__() == repr
