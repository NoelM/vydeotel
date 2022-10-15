from struct import pack


def bit_read(byte, pos):
    if byte > 255 or pos > 7:
        raise Exception

    mask = 1 << pos
    return 0 if (byte & mask) == 0 else 1


def bit_write(byte, pos, val):
    if byte > 255 or pos > 7 or val > 1:
        raise Exception

    if val == 0:
        return byte & ~(1 << pos)
    else:
        return byte | (1 << pos)


def write_byte(byte: int):
    even = False
    for i in range(7):
        if bit_read(byte, i) == 1:
            even = not even

    if even:
        byte = bit_write(byte, 7, 1)
    else:
        byte = bit_write(byte, 7, 0)

    return pack("B", byte)


def low_byte(word):
    if word > 65535:
        raise Exception

    return word & 255


def high_byte(word):
    if word > 65535:
        raise Exception

    return word >> 8


def display_vdt(minitel, filename):
    minitel.clean_screen()
    with open(filename, "rb") as fp:
        data = fp.read()
        for byte in data:
            minitel.write_byte(int(byte))


def between_bounds(value: int, min_bound: int, max_bound: int) -> int:
    """Return the value between the bounds included
        e.g. between_bounds(-1, 0, 10) -> 0
        and  between_bounds(11, 0, 10) -> 10

    :param value: an integer to keep between bounds
    :param min_bound: the value must be greater than or equal to it
    :param max_bound: the value must be less than or equal to it
    :return: the value bounded
    """
    if value < min_bound:
        return min_bound
    elif value > max_bound:
        return max_bound
    else:
        return value
