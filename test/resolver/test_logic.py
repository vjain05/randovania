from unittest.mock import MagicMock

import randovania.resolver.logic
from randovania.resolver.game_description import EventNode


def test_actions_with_reach_empty():
    state = MagicMock()
    memory = MagicMock(spec=randovania.resolver.logic.LogicMemory)
    game = MagicMock()

    options = list(randovania.resolver.logic.actions_with_reach([], state, memory, game))

    assert options == []


def test_actions_with_reach_no_resources():
    state = MagicMock()
    memory = MagicMock(spec=randovania.resolver.logic.LogicMemory)
    game = MagicMock()

    options = list(randovania.resolver.logic.actions_with_reach([MagicMock(), MagicMock()], state, memory, game))

    assert options == []


def test_actions_with_reach_with_event():
    state = MagicMock()
    memory = MagicMock(spec=randovania.resolver.logic.LogicMemory)
    game = MagicMock()
    event = MagicMock(spec=EventNode)
    state.has_resource.return_value = False

    # Run
    options = list(randovania.resolver.logic.actions_with_reach([event], state, memory, game))

    # Assert
    assert options == [event]
    event.resource.assert_called_once_with(game.resource_database)
    state.has_resource.assert_called_once_with(event.resource.return_value)
    memory.get_additional_requirements.assert_called_once_with(event)
    memory.get_additional_requirements.return_value.satisfied.assert_called_once_with(state.resources)