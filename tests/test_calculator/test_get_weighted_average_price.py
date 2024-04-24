import pytest

from sweepy.calculator import (
    get_weighted_average_lay_price,
    get_weighted_average_back_price,
    PriceSize,
)

from decimal import Decimal


@pytest.mark.parametrize(
    "list_of_price_sizes",
    [
        ([]),
        ([PriceSize(price=2.0, size=20), PriceSize(price=3.0, size=20)]),
        (
            [
                PriceSize(price=2.0, size=10),
                PriceSize(price=3.0, size=20),
                PriceSize(price=4.0, size=30),
            ]
        ),
    ],
)
def test_get_weighted_average_lay_price_invalid_input(list_of_price_sizes):
    assert get_weighted_average_lay_price(list_of_price_sizes).is_nan()


@pytest.mark.parametrize(
    "list_of_price_sizes, expected",
    [
        ([PriceSize(price=2.0, size=100)], Decimal("2.0")),
        (
            [PriceSize(price=2.0, size=100), PriceSize(price=3.0, size=200)],
            Decimal("2.0000"),
        ),
        (
            [PriceSize(price=2.0, size=50), PriceSize(price=3.0, size=200)],
            Decimal("2.5000"),
        ),
        (
            [PriceSize(price=2.0, size=70), PriceSize(price=3.0, size=100)],
            Decimal("2.3000"),
        ),
        (
            [PriceSize(price=2.0, size=90), PriceSize(price=4.0, size=100)],
            Decimal("2.2000"),
        ),
    ],
)
def test_get_weighted_average_lay_price_with_default_arguments(
    list_of_price_sizes, expected
):
    assert get_weighted_average_lay_price(list_of_price_sizes) == expected


@pytest.mark.parametrize(
    "list_of_price_sizes, expected",
    [
        ([PriceSize(price=2.0, size=100)], Decimal("2.0")),
        (
            [PriceSize(price=2.0, size=100), PriceSize(price=3.0, size=200)],
            Decimal("3.0"),
        ),
        (
            [PriceSize(price=2.0, size=50), PriceSize(price=1.5, size=200)],
            Decimal("1.75"),
        ),
        (
            [PriceSize(price=2.0, size=70), PriceSize(price=3.0, size=30)],
            Decimal("2.3000"),
        ),
        (
            [PriceSize(price=60.0, size=90), PriceSize(price=4.0, size=100)],
            Decimal("54.4000"),
        ),
    ],
)
def test_get_weighted_average_back_price_with_default_arguments(
    list_of_price_sizes, expected
):
    assert get_weighted_average_back_price(list_of_price_sizes) == expected
