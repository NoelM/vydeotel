package main

import "strings"

// Le standard Télétel

const MaxRetry = 3

const (
	ResolutionSimple = iota
	ResolutionDouble
)

const (
	ColonnesSimple = 40
	LignesSimple   = 25
	ColonnesDouble = 2 * ColonnesSimple
	LignesDouble   = 2 * LignesSimple
)

// 1 Mode Vidéotex
//
// 1.2.3 Codage des caractères visualisables
// Jeu G0 => alphanumérique (voir p.100)
// Jeu G1 => semi-graphique (voir p.101 et 102)
// Jeu G2 => complément à G0 (voir p.103)
// Les caractères du jeu G2 sont obtenus si précédés du code SS2 (0x19).
// On peut les afficher directement en utilisant printSpecialChar(byte b) :
const (
	Livre        = 0x23
	Dollar       = 0x24
	Diese        = 0x26
	Paragraphe   = 0x27
	FlecheGauche = 0x2C
	FlecheHaut   = 0x2D
	FlecheDroite = 0x2E
	FlecheBas    = 0x2F
	Degre        = 0x30
	PlusOuMoins  = 0x31
	Division     = 0x38
	UnQuart      = 0x3C
	UnDemi       = 0x3D
	TroisQuart   = 0x3E
	OeMajuscule  = 0x6A
	OeMinuscule  = 0x7A
	Beta         = 0x7B
)

// Les diacritiques ne peuvent pas être affichés seuls.
// printSpecialChar(byte b) n'aura donc aucun effet ici.
const (
	AccentGrave       = 0x41
	AccentAigu        = 0x42
	AccentCirconflexe = 0x43
	Trema             = 0x48
	Cedille           = 0x4B
)

// 1.2.4 Codage des attributs de visualisation (voir p.91)
// Ces fonctions sont obtenues si précédées du code ESC (0x1B).
// Nous avons alors accès à la grille C1. On peut y accéder directement
// en utilisant attributs(byte attribut).
// Couleur de caractère

const (
	CaractereNoir    = 0x40
	CaractereRouge   = 0x41
	CaractereVert    = 0x42
	CaractereJaune   = 0x43
	CaractereBleu    = 0x44
	CaractereMagenta = 0x45
	CaractereCyan    = 0x46
	CaractereBlanc   = 0x47
)

// Couleur de fond
// En mode texte, l'espace (0x20) est l'élément déclencheur du changement de couleur de fond (voir p.93). Ce changement est valide jusqu'à la fin d'une rangée.
const (
	FondNoir    = 0x50 // Pour éviter d'avoir cet espace à l'écran, une autre solution (dans ce cas le caractère sera noir), est de mettre en oeuvre le fond inversé.
	FondRouge   = 0x51 // Par exemple :
	FondVert    = 0x52 // minitel.attributs(CARACTERE_VERT);
	FondJaune   = 0x53 // minitel.attributs(INVERSION_FOND);
	FondBleu    = 0x54 // minitel.print("J'ECRIS ICI MON TEXTE");
	FondMagenta = 0x55 // minitel.attributs(FOND_NORMAL);
	FondCyan    = 0x56
	FondBlanc   = 0x57
)

// Taille
const (
	GrandeurNormale = 0x4C // Non utilisable en mode graphique
	DoubleHauteur   = 0x4D // Non utilisable en mode graphique
	DoubleLargeur   = 0x4E // Non utilisable en mode graphique
	DoubleGrandeur  = 0x4F // Non utilisable en mode graphique
)

// Clignotement ou fixité
const (
	Clignotement = 0x48
	Fixe         = 0x49
)

// Début et fin de masquage
const (
	Masquage   = 0x58
	Demasquage = 0x5F
)

// Début ou fin de lignage
const (
	FinLignage   = 0x59
	DebutLignage = 0x5A // En mode texte, l'espace (0x20) marque le début d'une zone de lignage. C'est l'élément déclencheur (voir p.93).
)

// Fond inversé ou normal
const (
	FondNormal    = 0x5C // Non utilisable en mode graphique
	InversionFond = 0x5D // Non utilisable en mode graphique
)

// Echappement vers la norme ISO 6429
const Csi = 0x1B5B

// 1.2.5 Fonctions de mise en page (voir p.94)
const (
	Bs = 0x08 // BackSpace : Déplacement du curseur d'un emplacement de caractère à gauche.
	Ht = 0x09 // Horizontal Tab : Déplacement du curseur d'un emplacement de caractère à droite.
	Lf = 0x0A // Line Feed : Déplacement du curseur d'un emplacement de caractère vers le bas.
	Vt = 0x0B // Vertical Tab : Déplacement du curseur d'un emplacement de caractère vers le haut.
	Cr = 0x0D // Carriage Return : Retour du curseur au début de la rangée courante.
)

// Les fonctions de type CSI sont développées à l'intérieur de la classe Minitel (plus bas).
const (
	Rs  = 0x1E // Record Separator : Retour du curseur en première position de la rangée 01. Ce code est un séparateur explicite d'article.
	Ff  = 0x0C // Form Feed : Retour du curseur en première position de la rangée 01 avec effacement complet de l'écran.
	Us  = 0x1F // Unit Separator : Séparateur de sous-article.
	Can = 0x18 // Cancel : Remplissage à partir de la position courante du curseur et jusqu'à la fin de la rangée par des espaces du jeu courant ayant l'état courant des attributs. La position courante du curseur n'est pas déplacée.
)

// 1.2.6 Autres fonctions (voir p.98)
// 1.2.6.1 Fonctions diverses :
const (
	Rep = 0x12 // Repetition : Permet de répéter le dernier caractère visualisé avec les attributs courants de la position active d'écriture.
	Nul = 0x00 // Null :
	Sp  = 0x20 // Space : Séparateur de zone possédant les mêmes attributs
	Del = 0x7F // Delete :
	Bel = 0x07 // Bell : Provoque l'émission d'un signal sonore
)

// 1.2.6.3 Fonctions d'extension de code
const (
	So  = 0x0E // Shift Out : Accès au jeu G1. => Mode semi-graphique
	Si  = 0x0F // Shift In : Accès au jeu G0.  => Mode alphanumérique
	Ss2 = 0x19 // Single Shift 2 : Appel d'un caractère unique du jeu G2.
	Esc = 0x1B // Escape : Echappement et accès à la grille C1.
)

// 1.2.6.4 Visualisation du curseur
const (
	Con  = 0x11 // Visualisation de la position active du curseur (curseur actif).
	Coff = 0x14 // Arrêt de la visualisation de la position active (curseur inactif).
)

// Chapitre 3 : Le clavier

// 6 Séquences émises par les touches de fonction en mode Vidéotex ou Mixte (voir p.123)
const (
	Special      = 0x13
	Envoi        = 0x1341
	Retour       = 0x1342
	Repetition   = 0x1343
	Guide        = 0x1344
	Annulation   = 0x1345
	Sommaire     = 0x1346
	Correction   = 0x1347
	Suite        = 0x1348
	ConnexionFin = 0x1359 // Non documenté
)

// 7 Codes et séquences émis par les touches de gestion du curseur et d'édition en mode Vidéotex ou Mixte (voir p.124)
const (
	ToucheFlecheHaut        = 0x1B5B41
	SuppressionLigne        = 0x1B5B4D
	ToucheFlecheBas         = 0x1B5B42
	InsertionLigne          = 0x1B5B4C
	ToucheFlecheDroite      = 0x1B5B43
	DebutInsertionCaractere = 0x1B5B3468
	FinInsertionCaractere   = 0x1B5B346C
	ToucheFlecheGauche      = 0x1B5B44
	SupressionCaractere     = 0x1B5B50
)

// Chapitre 6 : Le Protocole (voir p.134)

// 1 Généralités (voir p.134)
const (
	CodeEmissionEcran    = 0x50
	CodeEmissionClavier  = 0x51
	CodeEmissionModem    = 0x52
	CodeEmissionPrise    = 0x53
	CodeReceptionEcran   = 0x58
	CodeReceptionClavier = 0x59
	CodeReceptionModem   = 0x5A
	CodeReceptionPrise   = 0x5B
)

// 3 Commandes d'aiguillages et de blocage des modules
// 3.2 Format des commandes (voir p.135)
const (
	AiguillageOff = 0x60
	AiguillageOn  = 0x61
)

// 3.4 Demande de statut d'aiguillages des modules
const (
	To   = 0x62
	From = 0x63
)

// 8 Commandes relatives à la prise (voir p.141)
const (
	Prog          = 0x6B
	StatusVitesse = 0x74
)

// 9 Commandes relatives au clavier (voir p.141)
const Eten = 0x41 // Clavier en mode étendu

// 10 Commandes relatives à l'écran (voir p.142)
const Rouleau = 0x43 // Ecran en mode rouleau

// 11 Commandes relatives à plusieurs modules (voir p.143)
const (
	Start      = 0x69
	Stop       = 0x6A
	Minuscules = 0x45 // Mode minuscules / majuscules du clavier
)

// 12 Commandes Protocole relatives au changement de standard (voir p.144)
const (
	Mixte1  = 0x327D
	Mixte2  = 0x327E
	Telinfo = 0x317D
)

// 13 L'état initial du minitel
// 13.2 Sur réception d'une commande de reset
const Reset = 0x7F

// Constantes pour h_line et v_line
const (
	Center = 0
	Top    = 1
	Bottom = 2
	Left   = 3
	Right  = 4
	Up     = 5
	Down   = 6
)

// A ranger
const (
	Pro1 = 0x39
	Pro2 = 0x3A
	Pro3 = 0x3B
)

// Correspondance ASCII / Videotex
const CharTable = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_xabcdefghijklmnopqrstuvwxyz"

func GetVideotextCharByte(c byte) byte {
	return byte(strings.LastIndexByte(CharTable, c))
}

func IsValidChar(c byte) bool {
	return c >= Sp && c <= Del
}
