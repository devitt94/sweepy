from collections import defaultdict

import random
import math

from sweepy.models.runner_probability import RunnerProbability


def assign_selections_staggered(
    participants: list[str],
    selections: list[RunnerProbability],
) -> dict[str, list[RunnerProbability]]:
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
):
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

    return result


def assign_selections_random(
    participants: list[str],
    selections: list[RunnerProbability],
) -> dict[str, list[RunnerProbability]]:
    pass
