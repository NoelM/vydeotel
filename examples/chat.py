import sys
sys.path.append('../')
import vydeotel as vy
import asyncio

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

async def keyboard_event(minitel: vy.Minitel):
    buffer = ""
    while True:
        key = minitel.get_key_code()
        if key == vy.CONNEXION_FIN:
            print("CONNEXION FIN")
        elif key == vy.RETOUR:
            print("RETOUR")
        elif key == vy.GUIDE:
            print("GUIDE")
        elif input == vy.ENVOI:
            print("ENVOI")
            print(buffer)
            buffer = ""
        elif input == vy.SOMMAIRE:
            print("SOMMAIRE")
        else:
            input_buffer += chr(input)

asyncio.get_event_loop().run_until_complete(keyboard_event(minitel))
asyncio.get_event_loop().run_forever()