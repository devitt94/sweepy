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
