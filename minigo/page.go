package main

import "log"

type Page interface {
	Draw()
	NewKey(uint)
	Envoi() uint
	Retour() uint
	Repetition() uint
	Guide() uint
	Annulation() uint
	Sommaire() uint
	Correction() uint
	Suite() uint
	ConnexionFin() uint
}

type TestPage struct {
	mntl *Minitel
}

func NewTestPage(mntl *Minitel) TestPage {
	return TestPage{
		mntl: mntl,
	}
}

func (p *TestPage) Draw() {
	var buf []byte

	buf = append(buf, Ff) // Screen cleanup, cursor at 1,1, article separator
	//buf = GetMoveCursorReturn(buf, 1)
	//buf = GetTextZone(buf, []byte{DoubleGrandeur, InversionFond}, "TEST MINIGO")
	buf = GetMessage(buf, "TEST VIDEOTEXT .GO")
	buf = GetMoveCursorReturn(buf, 1)
	buf = GetMessage(buf, "Telematique 2000")
	buf = GetMoveCursorReturn(buf, 1)
	buf = GetMessage(buf, " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_abcdefghijklmnopqrstuvwxyz")

	p.mntl.SendBytes(buf)
}

func (p *TestPage) Envoi() uint {
	return 0
}

func (p *TestPage) Retour() uint {
	return 0
}

func (p *TestPage) Repetition() uint {
	return 0
}

func (p *TestPage) Guide() uint {
	return 0
}

func (p *TestPage) Annulation() uint {
	return 0
}

func (p *TestPage) Sommaire() uint {
	return 0
}

func (p *TestPage) Correction() uint {
	return 0
}

func (p *TestPage) Suite() uint {
	return 0
}

func (p *TestPage) ConnexionFin() uint {
	return 0
}

func (p *TestPage) NewKey(k uint) {
	log.Printf("got key: %d", k)
}
