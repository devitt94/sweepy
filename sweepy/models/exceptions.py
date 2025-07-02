class MarketNotFoundException(Exception):
    """Exception raised when a market is not found."""

    pass


class NotEnoughSelectionsException(Exception):
    """Exception raised when there are not enough selections for the number of participants."""

    pass

    def __init__(self, num_selections: int, num_participants: int):
        super().__init__(
            f"Not enough selections for the number of participants: {num_selections} < {num_participants}"
        )


class NotEnoughLiquidityException(Exception):
    """Exception raised when there is not enough liquidity in the market."""

    def __init__(self):
        super().__init__(
            "Not enough liquidity in the market to determine runner probabilities for a sweepstake."
        )
