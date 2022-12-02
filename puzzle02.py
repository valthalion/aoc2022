def read_data(test=False):
    filename = f'puzzle02{"-test" if test else ""}.in'
    with open(filename, 'r') as f:
        plays = [line.strip().split() for line in f]
    return plays


def decode1(plays):
    play = {'X': 'A', 'Y': 'B', 'Z': 'C'}
    return [(other, play[you]) for other, you in plays]


def decode2(plays):
    def play(other, you):
        other_num = ord(other) - ord('A')
        you_num = (other_num + (ord(you) - ord('X') - 1)) % 3
        return chr(ord('A') + you_num)
    return [(other, play(other, you)) for other, you in plays]


def score(game_rules, plays):
    total = 0
    for other_play, your_play in plays:
        result = game_rules['who_wins'][other_play][your_play]
        total += game_rules['play_value'][your_play] + game_rules['result_value'][result]
    return total


def part_1():
    game_rules = {
        'play_value' : {'A': 1, 'B': 2, 'C': 3},
        'result_value': {-1: 0, 0: 3, 1: 6},
        'who_wins': {
            'A': {'A': 0, 'B': 1, 'C': -1},
            'B': {'A': -1, 'B': 0, 'C': 1},
            'C': {'A': 1, 'B': -1, 'C': 0},
        }
    }
    plays = decode1(read_data(test=False))
    return score(game_rules, plays)


def part_2():
    game_rules = {
        'play_value' : {'A': 1, 'B': 2, 'C': 3},
        'result_value': {-1: 0, 0: 3, 1: 6},
        'who_wins': {
            'A': {'A': 0, 'B': 1, 'C': -1},
            'B': {'A': -1, 'B': 0, 'C': 1},
            'C': {'A': 1, 'B': -1, 'C': 0},
        }
    }
    plays = decode2(read_data(test=False))
    return score(game_rules, plays)
