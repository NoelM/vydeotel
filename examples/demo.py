import sys
import time

sys.path.append('../')
import vydeotel as vy


def splash(mntl: vy.Minitel, title: str, subtitle: str):
    mntl.clean_screen()
    mntl.move_cursor_xy(2, 5)
    mntl.set_attribute(vy.DOUBLE_GRANDEUR)
    mntl.println(title.upper())
    mntl.move_cursor_xy(2, 8)
    mntl.set_attribute(vy.DOUBLE_HAUTEUR)
    mntl.println(subtitle.upper())


def count_down_screen(mntl: vy.Minitel, squad: str, speaker: str, subtitle: str, duration: int):
    mntl.clean_screen()
    mntl.move_cursor_xy(2, 2)
    mntl.set_attribute(vy.DOUBLE_HAUTEUR)
    mntl.set_attribute(vy.INVERSION_FOND)
    mntl.println(f"{squad.upper()} // {speaker.upper()}")
    mntl.move_cursor_xy(2, 5)
    mntl.set_attribute(vy.INVERSION_FOND)
    mntl.set_attribute(vy.GRANDEUR_NORMALE)
    mntl.println(subtitle)

    count_down(mntl, duration)


def count_down(mntl: vy.Minitel, duration: int):
    mntl.move_cursor_xy(5, 10)
    mntl.set_attribute(vy.DOUBLE_GRANDEUR)
    for remaining in range(duration, -1):
        mntl.clear_line()
        mntl.print(f"{remaining}")
        time.sleep(1)


minitel = vy.Minitel("/dev/ttyS0")

splash(minitel, "DEMO", "SPRINT 22.15")
time.sleep(5)
splash(minitel, "SQUAD BLUE", "3 ORATEURS")
time.sleep(5)
count_down_screen(minitel, "BLUE", "TOTO", "TITI", 60)


