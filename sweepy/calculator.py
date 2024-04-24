from decimal import Decimal

from sweepy.models import Market, PriceSize, RunnerProbability

NUM_DECIMAL_PLACES = 4


def _get_weighted_average_price(
    list_of_price_sizes: list[PriceSize],
    min_size: Decimal = Decimal("1.0"),
    max_size: Decimal = Decimal("1.0"),
) -> Decimal:
    """
    Calculate the size-weighted average price from  a list of PriceSize objects up to 4 decimal.

    Args:
        list_of_price_sizes: A list of PriceSize objects.
        min_size: The minimum size to consider in the weighted average. If the total size of the list of PriceSize objects is less than this value, return NaN
        max_size: The size to consider in the weighted average. If the total size of the list of PriceSize objects is less than this value, only consider the best availability up to this size.
        decimal_places: The number of decimal places to round the result to.
    Returns:
        The weighted average price of the list of PriceSize objects.

    Examples:
        >>> _get_weighted_average_price([PriceSize(price=2.0, size=100), PriceSize(price=3.0, size=200)])
        Decimal('2.6667')
        >>> _get_weighted_average_price([PriceSize(price=2.0, size=100), PriceSize(price=3.0, size=200)], min_size=500)
        Decimal('nan')
        >>> _get_weighted_average_price([PriceSize(price=2.0, size=100), PriceSize(price=3.0, size=200)], max_size=100)
        Decimal('2.0')
        >>> _get_weighted_average_price([PriceSize(price=2.0, size=100), PriceSize(price=3.0, size=200)], max_size=150)
        Decimal('2.3333')
    """

    total_size = Decimal(0)
    weighted_sum = Decimal(0)
    for price_size in list_of_price_sizes:
        size_to_add = min(max_size - total_size, price_size.size)
        if size_to_add <= 0:
            break

        total_size += size_to_add
        weighted_sum += size_to_add * price_size.price

    if total_size < min_size:
        return Decimal("nan")

    result = weighted_sum / total_size
    return result.quantize(Decimal(f"1e-{NUM_DECIMAL_PLACES}"))


def get_weighted_average_lay_price(
    price_sizes: list[PriceSize],
) -> Decimal:
    price_sizes = sorted(price_sizes, key=lambda x: x.price)
    return _get_weighted_average_price(price_sizes)


def get_weighted_average_back_price(
    price_sizes: list[PriceSize],
) -> Decimal:
    price_sizes = sorted(price_sizes, key=lambda x: x.price, reverse=True)
    return _get_weighted_average_price(price_sizes)


def calculate_implied_probability(
    back_availability: list[PriceSize],
    lay_availability: list[PriceSize],
) -> Decimal:
    """
    Calculate the probability of a selection winning based on the back and lay availability.

    Args:
        back_availability: A list of PriceSize objects representing the back availability.
        lay_availability: A list of PriceSize objects representing the lay availability.
    Returns:
        The implied probability of the selection winning.

    Examples:
        >>> calculate_implied_probability([PriceSize(price=2.0, size=100), PriceSize(price=3.0, size=200)], [PriceSize(price=2.0, size=100), PriceSize(price=3.0, size=200)])
        Decimal('0.5')
        >>> calculate_implied_probability([PriceSize(price=2.0, size=300), PriceSize(price=3.0, size=200)], [PriceSize(price=2.0, size=100), PriceSize(price=3.0, size=200)])
        Decimal('0.5')
    """

    # Get size-weighted average back_price available
    back_price = get_weighted_average_back_price(back_availability)
    lay_price = get_weighted_average_lay_price(lay_availability)

    result = Decimal("2.0") / (back_price + lay_price)
    return result.quantize(Decimal(f"1e-{NUM_DECIMAL_PLACES}"))


def compute_market_probabilities(market: Market) -> list[RunnerProbability]:
    """
    Calculate the implied probabilities of each runner in a market.

    Args:
        market: A Market object representing the market to calculate the probabilities for.

    Returns:
        A list of RunnerProbability objects representing the implied probabilities of each runner in the market.
    """

    market_overround = Decimal(0)
    runner_probabilities = []
    for runner in market.runners:
        implied_probability = calculate_implied_probability(
            back_availability=runner.available_to_back,
            lay_availability=runner.available_to_lay,
        )

        if implied_probability.is_nan():
            implied_probability = Decimal("0.0")

        market_overround += implied_probability
        runner_probabilities.append((runner, implied_probability))

    return [
        RunnerProbability(
            runner=runner,
            implied=implied_probability,
            market_adjusted=(implied_probability / market_overround).quantize(
                implied_probability
            ),
        )
        for runner, implied_probability in runner_probabilities
    ]
