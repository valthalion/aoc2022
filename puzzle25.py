test = False


value = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
snafu_value = {v: k for k, v in value.items()}


def read_data():
    filename = f'puzzle25{"-test" if test else ""}.in'
    with open(filename, 'r') as f:
        numbers = [line.strip() for line in f]
    return numbers


def snafu2dec(number):
    total = 0
    for v in number:
        total *= 5
        total += value[v]
    return total


def dec2snafu(number):
    base5 = []
    while number:
        number, remainder = divmod(number, 5)
        base5.append(remainder)
    snafu = []
    carry = 0
    for value in base5:
        value += carry
        carry = 0
        while value > 5:
            carry += 1
            value -= 5
        if value <= 2:
            snafu.append(snafu_value[value])
        else:
            snafu.append(snafu_value[value - 5])
            carry += 1
    if carry:
        snafu.append(snafu_value[carry])
    return ''.join(reversed(snafu))


def part_1():
    return dec2snafu(sum(snafu2dec(number) for number in read_data()))

def part_2():
    pass
