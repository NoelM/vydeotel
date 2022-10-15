import random
import sys
import time

sys.path.append("../")
import videotext as vy
from utils import display_vdt


def splash_demo(mntl: vy.VideoText, sprint: str):
    mntl.clean_screen()
    mntl.set_attribute(vy.FIXE)
    display_vdt(mntl, "3615demo.vdt")

    mntl.text_mode()
    mntl.move_cursor_xy(8, 19)
    mntl.set_attribute(vy.CARACTERE_BLANC)
    mntl.set_attribute(vy.FOND_NORMAL)
    mntl.set_attribute(vy.DOUBLE_GRANDEUR)
    mntl.println(sprint.upper())


def splash_squad(mntl: vy.VideoText, squad_name: str, speakers: str):
    mntl.clean_screen()
    mntl.set_attribute(vy.FIXE)
    display_vdt(mntl, "squad.vdt")

    mntl.text_mode()
    mntl.move_cursor_xy(5, 15)
    mntl.set_attribute(vy.CARACTERE_BLANC)
    mntl.set_attribute(vy.FOND_NORMAL)
    mntl.set_attribute(vy.DOUBLE_GRANDEUR)
    mntl.println(squad_name.upper())

    mntl.move_cursor_xy(5, 18)
    mntl.set_attribute(vy.DOUBLE_LARGEUR)
    mntl.println(speakers.upper())


def count_down_screen(
    mntl: vy.VideoText, squad: str, speaker: str, line1: str, line2: str, duration: int
):
    mntl.clean_screen()
    mntl.set_attribute(vy.FIXE)
    mntl.move_cursor_xy(5, 2)
    mntl.set_attribute(vy.DOUBLE_HAUTEUR)
    mntl.println(f"{squad.upper()}")

    mntl.move_cursor_xy(5, 7)
    mntl.set_attribute(vy.DOUBLE_GRANDEUR)
    mntl.println(f"== {speaker.upper()} ==")

    mntl.move_cursor_xy(5, 8)
    mntl.set_attribute(vy.DOUBLE_HAUTEUR)
    mntl.println(line1)

    if line2 != "":
        mntl.move_cursor_xy(5, 10)
        mntl.set_attribute(vy.DOUBLE_HAUTEUR)
        mntl.println(line2)

    input("countdown press enter")
    count_down(mntl, duration)


def count_down(mntl: vy.VideoText, duration: int):
    mntl.set_attribute(vy.DOUBLE_GRANDEUR)
    for remaining in reversed(range(duration)):
        try:
            mntl.move_cursor_xy(15, 13)
            mntl.clear_line()
            mntl.move_cursor_xy(15, 15)

            m, s = divmod(remaining, 60)
            mntl.set_attribute(vy.DOUBLE_GRANDEUR)
            mntl.print("{:02d}:{:02d}".format(m, s))
            time.sleep(1)

            if remaining < 30:
                mntl.graphic_mode()
                for _ in range(10):
                    mntl.move_cursor_xy(random.randint(1, 40), random.randint(0, 25))
                    mntl.write_byte(0x5F)
                mntl.text_mode()

        except KeyboardInterrupt:
            break


minitel = vy.VideoText("/dev/ttyS0")
total_duration = 150

splash_demo(minitel, "SPRINT 22.16")
input("squad enter")
splash_squad(minitel, "GREEN", "1 SPEAKER")
input("speaker press enter")
count_down_screen(
    minitel,
    "SQUAD GREEN",
    "NABIL",
    "Visualization Card in Scenario ",
    "& KW Groups",
    total_duration,
)

input("squad enter")
splash_squad(minitel, "PINK", "2 SPEAKERS")
input("speaker press enter")
count_down_screen(
    minitel,
    "SQUAD PINK",
    "AUREL & AYMEN",
    "Airbyte MVP",
    "Connections from the Django Admin",
    2 * total_duration,
)

input("speaker press enter")
splash_squad(minitel, "BLUE", "3 SPEAKERS")
input("speaker press enter")
count_down_screen(minitel, "SQUAD BLUE", "YASSIN", "SEMRush", "", total_duration)
input("speaker press enter")
count_down_screen(minitel, "SQUAD BLUE", "HAIKEL", "Action Board", "", total_duration)
input("speaker press enter")
count_down_screen(minitel, "SQUAD BLUE", "STEPHANE", "Localization", "", total_duration)

input("speaker press enter")
splash_squad(minitel, "DATA ANALYTICS", "1 SPEAKER")
input("speaker press enter")
count_down_screen(
    minitel, "DATA ANALYTICS", "LEA", "KPIs for Data Quality", "", total_duration
)

input("speaker press enter")
splash_squad(minitel, "ORANGE", "2 SPEAKERS")
input("speaker press enter")
count_down_screen(
    minitel,
    "SQUAD ORANGE",
    "Sevket",
    "Template Preview",
    "New module selection modal",
    total_duration,
)
input("speaker press enter")
count_down_screen(
    minitel, "SQUAD ORANGE", "Younes", "PW Impact", "CWV investigation", total_duration
)

input("speaker press enter")
splash_squad(minitel, "RED", "2 SPEAKERS")
input("speaker press enter")
count_down_screen(
    minitel, "SQUAD RED", "Greg A", "Customize Recipients", "", total_duration
)
input("speaker press enter")
count_down_screen(
    minitel, "SQUAD RED", "Josselin", "Custom Alerts Flow", "", total_duration
)

input("speaker press enter")
splash_demo(minitel, "TOUS EN RETRO !")
