from randovania.game_description import RequirementSet


def test_empty_requirement_set():
    assert RequirementSet.empty().satisfied({})