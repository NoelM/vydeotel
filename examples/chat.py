import sys
sys.path.append('../')
import vydeotel as vy

minitel = vy.Minitel("/dev/ttyS0")

minitel.move_cursor_xy(0,0)
minitel.clean_screen()

minitel.println("")
minitel.set_attribute(vy.DOUBLE_GRANDEUR)
minitel.println("Messagerie")
minitel.set_attribute(vy.GRANDEUR_NORMALE)

minitel.println("Pseudo        ...............")
minitel.println("Mot de passe  ...............")

minitel.move_cursor_xy(15,3)
minitel.cursor()