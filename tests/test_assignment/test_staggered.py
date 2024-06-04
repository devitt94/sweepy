from sweepy.assignment import assign_selections_staggered


def test_assign_selections_tiered_each_selection_assigned_exactly_once(
    runner_probabilities_us_open,
):
    participants = ["Alice", "Bob", "Charlie", "David"]
    result = assign_selections_staggered(participants, runner_probabilities_us_open)

    all_assigned_selections = [
        selection for selections in result.values() for selection in selections
    ]

    assert len(all_assigned_selections) == len(runner_probabilities_us_open)
    assert len(set(all_assigned_selections)) == len(runner_probabilities_us_open)
