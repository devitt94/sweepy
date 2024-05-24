from collections import defaultdict

from decimal import Decimal
import random
import math

from sweepy.models.runner_probability import RunnerProbability


def assign_selections_staggered(
    participants: list[str],
    selections: list[RunnerProbability],
) -> dict[str, list[RunnerProbability]]:
    """
    Assign selections to participants in a staggered fashion, where the first participant gets the selection with the best odds,
    the second participant gets the selection , and so on. Once all participants
    have a selection, the process repeats with the participant with the lowest odds getting the next selection.
    """
    resulting_selections = defaultdict(list)

    selections_ordered_by_odds = sorted(selections, reverse=True)
    num_participants = len(participants)

    for i, selection in enumerate(selections_ordered_by_odds):
        participant_index = i % num_participants
        participant = participants[participant_index]

        resulting_selections[participant].append(selection)

        if participant_index == num_participants - 1:
            participants = list(reversed(participants))

    return resulting_selections


def assign_selections_tiered(
    participants: list[str],
    selections: list[RunnerProbability],
) -> dict[str, list[RunnerProbability]]:
    result = defaultdict(list)

    num_tiers = math.ceil(len(selections) / len(participants))
    selections_ordered_by_odds = sorted(selections, reverse=True)

    for tier_num in range(num_tiers):
        tier_start_index = tier_num * len(participants)
        tier_stop_index = (tier_num + 1) * len(participants)
        tier_selections = selections_ordered_by_odds[tier_start_index:tier_stop_index]

        random.shuffle(participants)
        for participant, selection in zip(participants, tier_selections):
            result[participant].append(selection)

    return dict(result)


def assign_selections_random(
    participants: list[str],
    selections: list[RunnerProbability],
) -> dict[str, list[RunnerProbability]]:
    result = defaultdict(list)

    random.shuffle(selections)
    random.shuffle(participants)

    for i in range(len(selections)):
        participant_index = i % len(participants)
        participant = participants[participant_index]
        selection = selections[i]

        result[participant].append(selection)

    return dict(result)


def assign_selections_fair(
    participants: list[str],
    selections: list[RunnerProbability],
) -> dict[str, list[RunnerProbability]]:
    """
    This function assigns selections to participants in a way the maximises fairness i.e. each participant has as close to the same
    expected value as possible.
    """
    result = {}

    target_probability = Decimal("1") / len(participants)
    selections_ordered_by_odds = sorted(selections, reverse=True)

    remaining_probabilities = {
        participant: target_probability for participant in participants
    }

    # Assign 1 of the top selections to each participant
    for participant in participants:
        result[participant] = []
        first_selection = selections_ordered_by_odds.pop(0)
        remaining_probabilities[participant] -= first_selection.market_adjusted
        result[participant].append(first_selection)

    random.shuffle(selections_ordered_by_odds)

    for selection in selections_ordered_by_odds:
        participant_with_most_remaining_probability = max(
            remaining_probabilities, key=remaining_probabilities.get
        )
        result[participant_with_most_remaining_probability].append(selection)
        remaining_probabilities[participant_with_most_remaining_probability] -= (
            selection.market_adjusted
        )

    return dict(result)
