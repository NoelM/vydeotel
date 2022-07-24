import vydeotel as vy

minitel = vy.Minitel("/dev/ttyS0")

minitel.write_byte(vy.DOUBLE_GRANDEUR)
minitel.println("Messagerie")
minitel.write_byte(vy.GRANDEUR_NORMALE)

minitel.println("Pseudo        ...............")
minitel.println("Mot de passe  ...............")