import pytest

from sweepy.calculator import calculate_implied_probability, PriceSize

from decimal import Decimal


@pytest.mark.parametrize(
    "back_availability, lay_availability",
    [
        ([], []),
        ([PriceSize(price=2.0, size=20), PriceSize(price=3.0, size=20)], []),
        (
            [
                PriceSize(price=2.0, size=10),
                PriceSize(price=3.0, size=20),
                PriceSize(price=4.0, size=30),
            ],
            [
                PriceSize(price=2.0, size=10),
                PriceSize(price=3.0, size=20),
                PriceSize(price=4.0, size=30),
            ],
        ),
    ],
)
def test_calculate_implied_probability_invalid_input(
    back_availability, lay_availability
):
    assert calculate_implied_probability(back_availability, lay_availability).is_nan()


@pytest.mark.parametrize(
    "back_availability, lay_availability, expected",
    [
        (
            [PriceSize(price=2.0, size=100)],
            [PriceSize(price=3.0, size=100)],
            Decimal("0.4"),
        ),
        (
            [PriceSize(price=2.0, size=100), PriceSize(price=3.0, size=200)],
            [PriceSize(price=4.0, size=50), PriceSize(price=5.0, size=200)],
            Decimal("0.2667"),
        ),
        (
            [PriceSize(price=75.0, size=2), PriceSize(price=50, size=200)],
            [
                PriceSize(price=300, size=10),
                PriceSize(price=340, size=20),
                PriceSize(price=500, size=300),
            ],
            Decimal("0.0040"),
        ),
        (
            [PriceSize(price=2.0, size=100), PriceSize(price=3.0, size=200)],
            [
                PriceSize(price=5.0, size=50),
                PriceSize(price=4.0, size=20),
                PriceSize(price=6.0, size=400),
            ],
            Decimal("0.2469"),
        ),
    ],
)
def test_calculate_implied_probability(back_availability, lay_availability, expected):
    assert (
        calculate_implied_probability(back_availability, lay_availability) == expected
    )
