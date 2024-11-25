import pytest

from tiffcomposer.core.coordinates import GeoCoordinate, GeoCoordinateError


def test_geocoordinate_initialization():
    coord = GeoCoordinate(10, 20)
    assert coord.latitude == 10
    assert coord.longitude == 20

    with pytest.raises(GeoCoordinateError):
        GeoCoordinate(-100, 20)

    with pytest.raises(GeoCoordinateError):
        GeoCoordinate(10, 200)


def test_geocoordinate_latitude_property():
    coord = GeoCoordinate(10, 20)
    assert coord.latitude == 10

    coord.latitude = 30
    assert coord.latitude == 30

    with pytest.raises(GeoCoordinateError):
        coord.latitude = -100


def test_geocoordinate_longitude_property():
    coord = GeoCoordinate(10, 20)
    assert coord.longitude == 20

    coord.longitude = 30
    assert coord.longitude == 30

    with pytest.raises(GeoCoordinateError):
        coord.longitude = 200


def test_geocoordinate_inverted():
    coord = GeoCoordinate(10, 20)
    inverted = coord.inverted
    assert inverted.latitude == 20
    assert inverted.longitude == 10


def test_geocoordinate_earth_radius():
    radius = GeoCoordinate.earth_radius(0)
    assert radius == pytest.approx(6378137.0, rel=1e-5)


def test_geocoordinate_distance_to():
    coord1 = GeoCoordinate(0, 0)
    coord2 = GeoCoordinate(0, 1)
    distance = coord1.distance_to(coord2)
    assert distance > 0


def test_geocoordinate_to_tuple():
    coord = GeoCoordinate(10, 20)
    assert coord.to_tuple() == (10, 20)


def test_geocoordinate_to_list():
    coord = GeoCoordinate(10, 20)
    assert coord.to_list() == [10, 20]


def test_geocoordinate_to_dict():
    coord = GeoCoordinate(10, 20)
    assert coord.to_dict() == {"latitude": 10, "longitude": 20}


def test_geocoordinate_from_tuple():
    coord = GeoCoordinate.from_tuple((10, 20))
    assert coord.latitude == 10
    assert coord.longitude == 20


def test_geocoordinate_from_list():
    coord = GeoCoordinate.from_list([10, 20])
    assert coord.latitude == 10
    assert coord.longitude == 20


def test_geocoordinate_from_dict():
    coord = GeoCoordinate.from_dict({"latitude": 10, "longitude": 20})
    assert coord.latitude == 10
    assert coord.longitude == 20


def test_geocoordinate_str():
    coord = GeoCoordinate(10, 20)
    assert str(coord) == "Latitude: 10, Longitude: 20"


def test_geocoordinate_repr():
    coord = GeoCoordinate(10, 20)
    assert repr(coord) == "GeoCoordinate(lat=10, lon=20)"


def test_geocoordinate_eq():
    coord1 = GeoCoordinate(10, 20)
    coord2 = GeoCoordinate(10, 20)
    assert coord1 == coord2


def test_geocoordinate_ne():
    coord1 = GeoCoordinate(10, 20)
    coord2 = GeoCoordinate(20, 30)
    assert coord1 != coord2


def test_geocoordinate_hash():
    coord1 = GeoCoordinate(10, 20)
    coord2 = GeoCoordinate(10, 20)
    assert hash(coord1) == hash(coord2)


def test_geocoordinate_add():
    coord1 = GeoCoordinate(10, 20)
    coord2 = GeoCoordinate(5, 5)
    result = coord1 + coord2
    assert result.latitude == 15
    assert result.longitude == 25


def test_geocoordinate_sub():
    coord1 = GeoCoordinate(10, 20)
    coord2 = GeoCoordinate(5, 5)
    result = coord1 - coord2
    assert result.latitude == 5
    assert result.longitude == 15
