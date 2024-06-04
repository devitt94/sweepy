from sweepy.assignment import assign_selections_tiered


def test_assign_selections_tiered_equal_number_of_selections(
    runner_probabilities_us_open,
):
    participants = ["Alice", "Bob", "Charlie", "David"]
    result = assign_selections_tiered(participants, runner_probabilities_us_open)

    min_selections = len(runner_probabilities_us_open) // len(participants)
    max_selections = min_selections + 1

    for _, selections in result.items():
        assert len(selections) in (min_selections, max_selections)


def test_assign_selections_tiered_each_selection_assigned_once(
    runner_probabilities_us_open,
):
    participants = ["Alice", "Bob", "Charlie", "David"]
    result = assign_selections_tiered(participants, runner_probabilities_us_open)

    all_assigned_selections = [
        selection for selections in result.values() for selection in selections
    ]

    assert len(all_assigned_selections) == len(runner_probabilities_us_open)
    assert len(set(all_assigned_selections)) == len(runner_probabilities_us_open)
