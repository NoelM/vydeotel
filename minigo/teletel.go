package main

import (
	"errors"
	"fmt"
)

const ByteParityPos = 7

func BitReadAt(b byte, i int) bool {
	return b&byte(1<<i) > 0
}

func GetByteLow(w int) byte {
	return byte(w & 0xFF)
}

func GetByteHigh(w int) byte {
	return byte(w >> 8)
}

func IsByteEven(b byte) bool {
	even := true
	for i := 0; i < ByteParityPos; i++ {
		if BitReadAt(b, i) {
			even = !even
		}
	}
	return even
}

func BitWriteAt(b byte, i int, value bool) byte {
	if value {
		return b | byte(1<<i)
	} else {
		return b &^ byte(1<<i)
	}
}

func GetByteWithParity(b byte) byte {
	// The parity bit is set to 0 if the sum of other bits is even,
	// thus if the sum is odd the parity bit is set to 1
	return BitWriteAt(b, ByteParityPos, !IsByteEven(b))
}

func CheckByteParity(b byte) (byte, error) {
	// The parity bit is set to 0 if the sum of other bits is even,
	// thus if the sum is odd the parity bit is set to 1
	if IsByteEven(b) && !BitReadAt(b, ByteParityPos) {
		return BitWriteAt(b, ByteParityPos, false), nil
	} else {
		return 0, errors.New("invalid parity received")
	}
}

func GetProCode(pro byte) (buf []byte, err error) {
	if pro < Pro1 || pro > Pro3 {
		return nil, errors.New("pro argument beyond bound [0x39;0x3B]")
	}
	buf = append(buf, GetByteWithParity(Esc))
	buf = append(buf, GetByteWithParity(pro))
	return
}

func GetPCode(i int) (buf []byte) {
	if i < 10 {
		buf = append(buf, GetByteWithParity(0x30+byte(i)))
	} else {
		buf = append(buf, GetByteWithParity(0x30+byte(i/10)))
		buf = append(buf, GetByteWithParity(0x30+byte(i%10)))
	}
	return
}

func GetWordWithParity(word int) (buf []byte) {
	buf = append(buf, GetByteWithParity(GetByteHigh(word)))
	buf = append(buf, GetByteWithParity(GetByteLow(word)))
	return
}

func IsPosInBounds(x, y int, resolution uint) (bool, error) {
	switch resolution {
	case ResolutionSimple:
		return x > 0 && x <= ColonnesSimple && y > 0 && y <= LignesSimple, nil
	case ResolutionDouble:
		return x > 0 && x <= ColonnesDouble && y > 0 && y <= ColonnesSimple, nil
	default:
		return false, fmt.Errorf("unknown resolution: %d", resolution)
	}
}

func GetMoveCursorXY(x, y int) (buf []byte) {
	buf = append(buf, GetWordWithParity(Csi)...)
	buf = append(buf, GetPCode(y)...)
	buf = append(buf, GetByteWithParity(0x3B))
	buf = append(buf, GetPCode(x)...)
	buf = append(buf, GetByteWithParity(0x48))
	return
}

func GetMoveCursorLeft(n int) (buf []byte) {
	if n == 1 {
		return []byte{GetByteWithParity(Bs)}
	} else {
		buf = append(buf, GetWordWithParity(Csi)...)
		buf = append(buf, GetPCode(n)...)
		buf = append(buf, GetByteWithParity(0x44))
	}
	return
}

func GetMoveCursorRight(n int) (buf []byte) {
	if n == 1 {
		return []byte{GetByteWithParity(Ht)}
	} else {
		buf = append(buf, GetWordWithParity(Csi)...)
		buf = append(buf, GetPCode(n)...)
		buf = append(buf, GetByteWithParity(0x43))
	}
	return
}

func GetMoveCursorDown(n int) (buf []byte) {
	if n == 1 {
		return []byte{GetByteWithParity(Lf)}
	} else {
		buf = append(buf, GetWordWithParity(Csi)...)
		buf = append(buf, GetPCode(n)...)
		buf = append(buf, GetByteWithParity(0x42))
	}
	return
}

func GetMoveCursorUp(n int) (buf []byte) {
	if n == 1 {
		return []byte{GetByteWithParity(Vt)}
	} else {
		buf = append(buf, GetWordWithParity(Csi)...)
		buf = append(buf, GetPCode(n)...)
		buf = append(buf, GetByteWithParity(0x41))
	}
	return
}

func GetMoveCursorReturn(n int) (buf []byte) {
	buf = append(buf, GetByteWithParity(Cr))
	buf = append(buf, GetMoveCursorDown(n)...)
	return
}

func GetCleanScreen() (buf []byte) {
	buf = append(buf, GetWordWithParity(Csi)...)
	buf = append(buf, GetByteWithParity(0x32), GetByteWithParity(0x4A))
	return
}

func GetCleanScreenFromCursor() (buf []byte) {
	buf = append(buf, GetWordWithParity(Csi)...)
	buf = append(buf, GetByteWithParity(0x4A))
	return
}

func GetCleanScreenToCursor() (buf []byte) {
	buf = append(buf, GetWordWithParity(Csi)...)
	buf = append(buf, GetByteWithParity(0x31), GetByteWithParity(0x4A))
	return
}

func GetCleanLine() (buf []byte) {
	buf = append(buf, GetWordWithParity(Csi)...)
	buf = append(buf, GetByteWithParity(0x32), GetByteWithParity(0x4B))
	return
}

func GetCleanLineFromCursor() (buf []byte) {
	buf = append(buf, GetWordWithParity(Csi)...)
	buf = append(buf, GetByteWithParity(0x4B))
	return
}

func GetCleanLineToCursor() (buf []byte) {
	buf = append(buf, GetWordWithParity(Csi)...)
	buf = append(buf, GetByteWithParity(0x31), GetByteWithParity(0x4B))
	return
}

func GetChar(c int32) (byte, error) {
	vdtByte := GetVideotextCharByte(byte(c))
	if IsValidChar(vdtByte) {
		return vdtByte, nil
	}
	return 0, errors.New("invalid char byte")
}

func GetMessage(msg string) (buf []byte, err error) {
	for _, c := range msg {
		if b, err := GetChar(c); err == nil {
			buf = append(buf, GetByteWithParity(b))
		} else {
			return nil, fmt.Errorf("ignored char %d: %w", c, err)
		}
	}
	return
}

type Minitel struct {
	fontSize   byte
	resolution uint
	driver     Driver
}

func (m *Minitel) MoveCursorXY(x, y int) error {
	inBound, err := IsPosInBounds(x, y, m.resolution)
	if err != nil {
		return fmt.Errorf("unable to move cursor: %w", err)
	}
	if !inBound {
		return fmt.Errorf("unable to move cursor: values (x=%d,y=%d) out of bound", x, y)
	}

	return m.driver.Send(GetMoveCursorXY(x, y))
}

func (m *Minitel) MoveCursorLeft(n int) error {
	return m.driver.Send(GetMoveCursorLeft(n))
}

func (m *Minitel) MoveCursorRight(n int) error {
	return m.driver.Send(GetMoveCursorRight(n))
}

func (m *Minitel) MoveCursorDown(n int) error {
	return m.driver.Send(GetMoveCursorDown(n))
}

func (m *Minitel) MoveCursorUp(n int) error {
	return m.driver.Send(GetMoveCursorUp(n))
}

func (m *Minitel) MoveCursorReturn(n int) error {
	return m.driver.Send(GetMoveCursorReturn(n))
}

func (m *Minitel) CleanScreen() error {
	return m.driver.Send(GetCleanScreen())
}

func (m *Minitel) CleanScreenFromCursor() error {
	return m.driver.Send(GetCleanLineFromCursor())
}

func (m *Minitel) CleanScreenToCursor() error {
	return m.driver.Send(GetCleanScreenToCursor())
}

func (m *Minitel) CleanLine() error {
	return m.driver.Send(GetCleanLine())
}

func (m *Minitel) CleanLineFromCursor() error {
	return m.driver.Send(GetCleanLineFromCursor())
}

func (m *Minitel) CleanLineToCursor() error {
	return m.driver.Send(GetCleanLineToCursor())
}

func (m *Minitel) PrintChar(c int32) error {
	var char byte
	var err error
	if char, err = GetChar(c); err != nil {
		return fmt.Errorf("unable to send char: %w", err)
	}
	return m.driver.Send([]byte{char})
}

func (m *Minitel) PrintMessage(msg string) error {
	var msgEncoded []byte
	var err error
	if msgEncoded, err = GetMessage(msg); err != nil {
		return fmt.Errorf("unable to send message: %w", err)
	}
	return m.driver.Send(msgEncoded)
}
