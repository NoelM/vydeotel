# Le standard Télétel

# 1 Mode Vidéotex

# 1.2.3 Codage des caractères visualisables
# Jeu G0 => alphanumérique (voir p.100)
# Jeu G1 => semi-graphique (voir p.101 et 102)
# Jeu G2 => complément à G0 (voir p.103)
# Les caractères du jeu G2 sont obtenus si précédés du code SS2 (0x19).
# On peut les afficher directement en utilisant printSpecialChar(byte b) :
LIVRE = 0x23
DOLLAR = 0x24
DIESE = 0x26
PARAGRAPHE = 0x27
FLECHE_GAUCHE = 0x2C
FLECHE_HAUT = 0x2D
FLECHE_DROITE = 0x2E
FLECHE_BAS = 0x2F
DEGRE = 0x30
PLUS_OU_MOINS = 0x31
DIVISION = 0x38
UN_QUART = 0x3C
UN_DEMI = 0x3D
TROIS_QUART = 0x3E
OE_MAJUSCULE = 0x6A
OE_MINUSCULE = 0x7A
BETA = 0x7B
# Les diacritiques ne peuvent pas être affichés seuls.
# printSpecialChar(byte b) n'aura donc aucun effet ici.
ACCENT_GRAVE = 0x41
ACCENT_AIGU = 0x42
ACCENT_CIRCONFLEXE = 0x43
TREMA = 0x48
CEDILLE = 0x4B

# 1.2.4 Codage des attributs de visualisation (voir p.91)
# Ces fonctions sont obtenues si précédées du code ESC (0x1B).
# Nous avons alors accès à la grille C1. On peut y accéder directement
# en utilisant attributs(byte attribut).
# Couleur de caractère
CARACTERE_NOIR = 0x40
CARACTERE_ROUGE = 0x41
CARACTERE_VERT = 0x42
CARACTERE_JAUNE = 0x43
CARACTERE_BLEU = 0x44
CARACTERE_MAGENTA = 0x45
CARACTERE_CYAN = 0x46
CARACTERE_BLANC = 0x47
# Couleur de fond                # En mode texte, l'espace (0x20) est l'élément déclencheur du changement de couleur de fond (voir p.93). Ce changement est valide jusqu'à la fin d'une rangée.
FOND_NOIR = 0x50  # Pour éviter d'avoir cet espace à l'écran, une autre solution (dans ce cas le caractère sera noir), est de mettre en oeuvre le fond inversé.
FOND_ROUGE = 0x51  # Par exemple :
FOND_VERT = 0x52  # minitel.attributs(CARACTERE_VERT);
FOND_JAUNE = 0x53  # minitel.attributs(INVERSION_FOND);
FOND_BLEU = 0x54  # minitel.print("J'ECRIS ICI MON TEXTE");
FOND_MAGENTA = 0x55  # minitel.attributs(FOND_NORMAL);
FOND_CYAN = 0x56
FOND_BLANC = 0x57
# Taille
GRANDEUR_NORMALE = 0x4C  # Non utilisable en mode graphique
DOUBLE_HAUTEUR = 0x4D  # Non utilisable en mode graphique
DOUBLE_LARGEUR = 0x4E  # Non utilisable en mode graphique
DOUBLE_GRANDEUR = 0x4F  # Non utilisable en mode graphique
# Clignotement ou fixité
CLIGNOTEMENT = 0x48
FIXE = 0x49
# Début et fin de masquage
MASQUAGE = 0x58
DEMASQUAGE = 0x5F
# Début ou fin de lignage
FIN_LIGNAGE = 0x59
DEBUT_LIGNAGE = 0x5A  # En mode texte, l'espace (0x20) marque le début d'une zone de lignage. C'est l'élément déclencheur (voir p.93).
# Fond inversé ou normal
FOND_NORMAL = 0x5C  # Non utilisable en mode graphique
INVERSION_FOND = 0x5D  # Non utilisable en mode graphique
# Echappement vers la norme ISO 6429
CSI = 0x1B5B

# 1.2.5 Fonctions de mise en page (voir p.94)
BS = 0x08  # BackSpace : Déplacement du curseur d'un emplacement de caractère à gauche.
HT = 0x09  # Horizontal Tab : Déplacement du curseur d'un emplacement de caractère à droite.
LF = 0x0A  # Line Feed : Déplacement du curseur d'un emplacement de caractère vers le bas.
VT = 0x0B  # Vertical Tab : Déplacement du curseur d'un emplacement de caractère vers le haut.
CR = 0x0D  # Carriage Return : Retour du curseur au début de la rangée courante.
# Les fonctions de type CSI sont développées à l'intérieur de la classe Minitel (plus bas).
RS = 0x1E  # Record Separator : Retour du curseur en première position de la rangée 01. Ce code est un séparateur explicite d'article.
FF = 0x0C  # Form Feed : Retour du curseur en première position de la rangée 01 avec effacement complet de l'écran.
US = 0x1F  # Unit Separator : Séparateur de sous-article.
CAN = 0x18  # Cancel : Remplissage à partir de la position courante du curseur et jusqu'à la fin de la rangée par des espaces du jeu courant ayant l'état courant des attributs. La position courante du curseur n'est pas déplacée.

# 1.2.6 Autres fonctions (voir p.98)
# 1.2.6.1 Fonctions diverses :
REP = 0x12  # Repetition : Permet de répéter le dernier caractère visualisé avec les attributs courants de la position active d'écriture.
NUL = 0x00  # Null :
SP = 0x20  # Space :
DEL = 0x7F  # Delete :
BEL = 0x07  # Bell : Provoque l'émission d'un signal sonore
# 1.2.6.3 Fonctions d'extension de code
SO = 0x0E  # Shift Out : Accès au jeu G1. => Mode semi-graphique
SI = 0x0F  # Shift In : Accès au jeu G0.  => Mode alphanumérique
SS2 = 0x19  # Single Shift 2 : Appel d'un caractère unique du jeu G2.
ESC = 0x1B  # Escape : Echappement et accès à la grille C1.
# 1.2.6.4 Visualisation du curseur
CON = 0x11  # Visualisation de la position active du curseur (curseur actif).
COFF = 0x14  # Arrêt de la visualisation de la position active (curseur inactif).

# Chapitre 3 : Le clavier

# 6 Séquences émises par les touches de fonction en mode Vidéotex ou Mixte (voir p.123)
SPECIAL = 0x13
ENVOI = 0x1341
RETOUR = 0x1342
REPETITION = 0x1343
GUIDE = 0x1344
ANNULATION = 0x1345
SOMMAIRE = 0x1346
CORRECTION = 0x1347
SUITE = 0x1348
CONNEXION_FIN = 0x1359  # Non documenté

# 7 Codes et séquences émis par les touches de gestion du curseur et d'édition en mode Vidéotex ou Mixte (voir p.124)
TOUCHE_FLECHE_HAUT = 0x1B5B41
SUPPRESSION_LIGNE = 0x1B5B4D
TOUCHE_FLECHE_BAS = 0x1B5B42
INSERTION_LIGNE = 0x1B5B4C
TOUCHE_FLECHE_DROITE = 0x1B5B43
DEBUT_INSERTION_CARACTERE = 0x1B5B3468
FIN_INSERTION_CARACTERE = 0x1B5B346C
TOUCHE_FLECHE_GAUCHE = 0x1B5B44
SUPRESSION_CARACTERE = 0x1B5B50

# Chapitre 6 : Le Protocole (voir p.134)

# 1 Généralités (voir p.134)
CODE_EMISSION_ECRAN = 0x50
CODE_EMISSION_CLAVIER = 0x51
CODE_EMISSION_MODEM = 0x52
CODE_EMISSION_PRISE = 0x53
CODE_RECEPTION_ECRAN = 0x58
CODE_RECEPTION_CLAVIER = 0x59
CODE_RECEPTION_MODEM = 0x5A
CODE_RECEPTION_PRISE = 0x5B

# 3 Commandes d'aiguillages et de blocage des modules
# 3.2 Format des commandes (voir p.135)
AIGUILLAGE_OFF = 0x60
AIGUILLAGE_ON = 0x61
# 3.4 Demande de statut d'aiguillages des modules
TO = 0x62
FROM = 0x63

# 8 Commandes relatives à la prise (voir p.141)
PROG = 0x6B
STATUS_VITESSE = 0x74

# 9 Commandes relatives au clavier (voir p.141)
ETEN = 0x41  # Clavier en mode étendu

# 10 Commandes relatives à l'écran (voir p.142)
ROULEAU = 0x43  # Ecran en mode rouleau

# 11 Commandes relatives à plusieurs modules (voir p.143)
START = 0x69
STOP = 0x6A
MINUSCULES = 0x45  # Mode minuscules / majuscules du clavier

# 12 Commandes Protocole relatives au changement de standard  (voir p.144)
MIXTE1 = 0x327D
MIXTE2 = 0x327E
TELINFO = 0x317D

# 13 L'état initial du minitel
# 13.2 Sur réception d'une commande de reset
RESET = 0x7F

# Constantes pour h_line et v_line
CENTER = 0
TOP = 1
BOTTOM = 2
LEFT = 3
RIGHT = 4
UP = 5
DOWN = 6

# Correspondance ASCII / Videotex
CHAR_TABLE = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_xabcdefghijklmnopqrstuvwxyz"


def get_char_byte(char):
    return CHAR_TABLE.rfind(char)


def is_valid_char(byte):
    return byte >= SP and byte <= DEL
