from enum import Enum


class AssignmentMethod(str, Enum):
    STAGGERED = "staggered"
    TIERED = "tiered"
    RANDOM = "random"
    FAIR = "fair"
