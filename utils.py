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
