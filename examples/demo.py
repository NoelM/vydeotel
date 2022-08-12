import sys
import time

sys.path.append('../')
import minitel as vy
from utils import display_vdt


def splash_demo(mntl: vy.Minitel, sprint: str):
    mntl.clean_screen()
    mntl.set_attribute(vy.FIXE)
    display_vdt(mntl, "3615demo.vdt")

    mntl.text_mode()
    mntl.move_cursor_xy(8, 19)
    mntl.set_attribute(vy.CARACTERE_BLANC)
    mntl.set_attribute(vy.FOND_NORMAL)
    mntl.set_attribute(vy.DOUBLE_GRANDEUR)
    mntl.println(sprint.upper())

def splash_squad(mntl: vy.Minitel, squad_name: str, speakers: str):
    mntl.clean_screen()
    mntl.set_attribute(vy.FIXE)
    display_vdt(mntl, "squad.vdt")

    mntl.text_mode()
    mntl.move_cursor_xy(8, 13)
    mntl.set_attribute(vy.CARACTERE_NOIR)
    mntl.set_attribute(vy.FOND_BLANC)
    mntl.set_attribute(vy.DOUBLE_GRANDEUR)
    mntl.println(squad_name.upper())

    mntl.move_cursor_xy(8, 17)
    mntl.set_attribute(vy.CARACTERE_BLANC)
    mntl.set_attribute(vy.FOND_NORMAL)
    mntl.set_attribute(vy.DOUBLE_LARGEUR)
    mntl.println(speakers.upper())


def count_down_screen(mntl: vy.Minitel, squad: str, speaker: str, subtitle: str, duration: int):
    mntl.clean_screen()
    mntl.set_attribute(vy.FIXE)
    mntl.move_cursor_xy(5, 3)
    mntl.set_attribute(vy.DOUBLE_HAUTEUR)
    mntl.println(f"{squad.upper()}")

    mntl.move_cursor_xy(5, 7)
    mntl.set_attribute(vy.DOUBLE_GRANDEUR)
    mntl.println(f"{speaker.upper()}")
    mntl.move_cursor_xy(5, 8)

    mntl.set_attribute(vy.DOUBLE_HAUTEUR)
    mntl.println(subtitle)

    input("countdown press enter")
    count_down(mntl, duration)


def count_down(mntl: vy.Minitel, duration: int):
    mntl.set_attribute(vy.DOUBLE_GRANDEUR)
    for remaining in reversed(range(duration)):
        try:
            mntl.move_cursor_xy(15, 13)
            mntl.clear_line()
            mntl.move_cursor_xy(15, 15)

            m, s = divmod(remaining, 60)
            mntl.print("{:02d}:{:02d}".format(m, s))
            time.sleep(1)

            if remaining == 30:
                mntl.set_attribute(vy.CLIGNOTEMENT)
                mntl.set_attribute(vy.DOUBLE_HAUTEUR)
                mntl.move_cursor_xy(13, 20)
                mntl.println("< 30 SECONDES")
                mntl.set_attribute(vy.FIXE)
                mntl.set_attribute(vy.DOUBLE_GRANDEUR)
        except KeyboardInterrupt:
            break


minitel = vy.Minitel("/dev/ttyS0")
total_duration = 20

splash_demo(minitel, "DEMO", "SPRINT 22.15")
input("squad enter")
splash_demo(minitel, "SQUAD BLUE", "2 ORATEURS")
input("speaker press enter")
count_down_screen(minitel, "SQUAD BLUE", "Yassin", "New widgets in Explorer Trends", total_duration)
input("speaker press enter")
count_down_screen(minitel, "SQUAD BLUE", "Stephane", "Locale middleware, expire date, localization", total_duration)

input("speaker press enter")
splash_demo(minitel, "SQUAD BLACK", "1 ORATEUR")
input("speaker press enter")
count_down_screen(minitel, "SQUAD BLACK", "Anthony", "Activation URL tester", total_duration)

input("speaker press enter")
splash_demo(minitel, "DATA ANALYTICS", "1 ORATEUR")
input("speaker press enter")
count_down_screen(minitel, "DATA ANALYTICS", "Efrain", "Present a use case", total_duration)

input("speaker press enter")
splash_demo(minitel, "SQUAD ORANGE", "3 ORATEURS")
input("speaker press enter")
count_down_screen(minitel, "SQUAD ORANGE", "Younes", "Insertion Strategy", total_duration)

input("speaker press enter")
count_down_screen(minitel, "SQUAD ORANGE", "Sevket", "Templates PW", total_duration)

input("speaker press enter")
count_down_screen(minitel, "SQUAD ORANGE", "Camille", "Infra PW and DX subjects", total_duration)

input("speaker press enter")
splash_demo(minitel, "MERCI ET BON WEEK-END", "TOUS EN RETRO !")
