import pytest
from main import Players, Country, GameProcess, dot_init, dots_init


def test_game_sprite_creation():
    sprite = dot_init(0)
    assert sprite.counter == 0
    assert sprite.obj == ''


def test_game_process_initialization():
    dots = dots_init()
    players = [Players(dots, 1), Players(dots, 2)]
    analyser = Country(dots, [players[0], players[1]])
    game_process = GameProcess(players, dots, analyser)
    assert len(game_process.players) == 2
    assert len(game_process.dots) == len(dots)


def test_move_peasant():
    dots = dots_init()
    count1 = 0
    count2 = 0
    for dot in dots:
        if dot.obj == '' and dot.land != 0:
            count1 = dot.counter
            break
    for friend in dots[count1].friends:
        if dots[friend].obj == '' and dots[friend].land != 0:
            count2 = dots[friend].counter
    dots[count1].state = 1
    dots[count2].state = 1
    dots[count1].blocked = 0
    dots[count2].blocked = 0
    dots[count1].change_object('peasant')
    player = Players(dots, state=1, money=10)
    player.move(count1, count2)
    assert dots[count1].obj == ''
    assert dots[count2].obj == 'peasant'


@pytest.fixture
def game_setup():
    dots = dots_init()
    players = [Players(dots, 1, money=20), Players(dots, 2, money=20)]
    analyser = Country(dots, [players[0], players[1]])
    game_process = GameProcess(players, dots, analyser)
    return game_process


def test_game_process_bots(game_setup):
    game_setup.bots()
    for player in game_setup.players:
        assert player.money >= 0  # Ensure players do not go into negative money
