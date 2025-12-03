import random
import string

from core.enums import RegionNames, RegionCodes
from core.regions.entities.region import Region
import pytest


class TestRegionEntity:

    def test_create_region_entity_success(self, pk_id):
        """ Тест на успешное создание сущности RegionEntity. """

        region = Region(
            id=pk_id,
            name=RegionNames.MOSCOW,
            code=RegionCodes.MOSCOW77
        )
        assert region.id == pk_id
        assert region.name == RegionNames.MOSCOW
        assert region.code == RegionCodes.MOSCOW77

    @pytest.mark.parametrize(
        "region_name,region_code,expectation",
        [
            (1, 2, pytest.raises(TypeError)),
            (random.choices(string.ascii_letters), random.choices(string.ascii_letters), pytest.raises(TypeError)),
            (tuple(), list(), pytest.raises(TypeError)),
        ],
    )
    def test_create_user_entity_exception(self, region_name, region_code, expectation, pk_id):
        """ Тест на вызов ошибки при создании сущности UserEntity с невалидными значениями email. """
        with expectation:
            Region(
                id=pk_id,
                name=random.choices(string.ascii_letters),
                code=random.choices(string.ascii_letters),
            )