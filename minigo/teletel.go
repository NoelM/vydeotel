package main

import (
	"errors"
	"fmt"
	"time"
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

func GetProCode(buf []byte, pro byte) ([]byte, error) {
	if pro < Pro1 || pro > Pro3 {
		return nil, errors.New("pro argument beyond bound [0x39;0x3B]")
	}
	buf = append(buf, GetByteWithParity(Esc))
	buf = append(buf, GetByteWithParity(pro))
	return buf, nil
}

func GetPCode(buf []byte, i int) []byte {
	if i < 10 {
		buf = append(buf, GetByteWithParity(0x30+byte(i)))
	} else {
		buf = append(buf, GetByteWithParity(0x30+byte(i/10)))
		buf = append(buf, GetByteWithParity(0x30+byte(i%10)))
	}
	return buf
}

func GetWordWithParity(buf []byte, word int) []byte {
	buf = append(buf, GetByteWithParity(GetByteHigh(word)))
	buf = append(buf, GetByteWithParity(GetByteLow(word)))
	return buf
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

func GetMoveCursorXY(buf []byte, x, y int) []byte {
	buf = GetWordWithParity(buf, Csi)
	buf = GetPCode(buf, y)
	buf = append(buf, GetByteWithParity(0x3B))
	buf = GetPCode(buf, x)
	buf = append(buf, GetByteWithParity(0x48))
	return buf
}

func GetMoveCursorLeft(buf []byte, n int) []byte {
	if n == 1 {
		return append(buf, GetByteWithParity(Bs))
	} else {
		buf = GetWordWithParity(buf, Csi)
		buf = GetPCode(buf, n)
		buf = append(buf, GetByteWithParity(0x44))
	}
	return buf
}

func GetMoveCursorRight(buf []byte, n int) []byte {
	if n == 1 {
		return append(buf, GetByteWithParity(Ht))
	} else {
		buf = GetWordWithParity(buf, Csi)
		buf = GetPCode(buf, n)
		buf = append(buf, GetByteWithParity(0x43))
	}
	return buf
}

func GetMoveCursorDown(buf []byte, n int) []byte {
	if n == 1 {
		return append(buf, GetByteWithParity(Lf))
	} else {
		buf = GetWordWithParity(buf, Csi)
		buf = GetPCode(buf, n)
		buf = append(buf, GetByteWithParity(0x42))
	}
	return buf
}

func GetMoveCursorUp(buf []byte, n int) []byte {
	if n == 1 {
		return append(buf, GetByteWithParity(Vt))
	} else {
		buf = GetWordWithParity(buf, Csi)
		buf = GetPCode(buf, n)
		buf = append(buf, GetByteWithParity(0x41))
	}
	return buf
}

func GetMoveCursorReturn(buf []byte, n int) []byte {
	buf = append(buf, GetByteWithParity(Cr))
	buf = GetMoveCursorDown(buf, n)
	return buf
}

func GetCleanScreen(buf []byte) []byte {
	buf = GetWordWithParity(buf, Csi)
	buf = append(buf, GetByteWithParity(0x32), GetByteWithParity(0x4A))
	return buf
}

func GetCleanScreenFromCursor(buf []byte) []byte {
	buf = GetWordWithParity(buf, Csi)
	buf = append(buf, GetByteWithParity(0x4A))
	return buf
}

func GetCleanScreenToCursor(buf []byte) []byte {
	buf = GetWordWithParity(buf, Csi)
	buf = append(buf, GetByteWithParity(0x31), GetByteWithParity(0x4A))
	return buf
}

func GetCleanLine(buf []byte) []byte {
	buf = GetWordWithParity(buf, Csi)
	buf = append(buf, GetByteWithParity(0x32), GetByteWithParity(0x4B))
	return buf
}

func GetCleanLineFromCursor(buf []byte) []byte {
	buf = GetWordWithParity(buf, Csi)
	buf = append(buf, GetByteWithParity(0x4B))
	return buf
}

func GetCleanLineToCursor(buf []byte) []byte {
	buf = append(buf, GetWordWithParity(buf, Csi)...)
	buf = append(buf, GetByteWithParity(0x31), GetByteWithParity(0x4B))
	return buf
}

func GetChar(c int32) (byte, error) {
	vdtByte := GetVideotextCharByte(byte(c))
	if IsValidChar(vdtByte) {
		return vdtByte, nil
	}
	return 0, errors.New("invalid char byte")
}

func GetMessage(buf []byte, msg string) ([]byte, error) {
	for _, c := range msg {
		if b, err := GetChar(c); err == nil {
			buf = append(buf, GetByteWithParity(b))
		} else {
			return nil, fmt.Errorf("ignored char %d: %w", c, err)
		}
	}
	return buf, nil
}

type Minitel struct {
	fontSize   byte
	resolution uint
	buffer     []byte
	driver     Driver
}

func (m *Minitel) clearBuffer() {
	m.buffer = []byte{}
}

func (m *Minitel) sendBuffer() error {
	return m.driver.Send(m.buffer)
}

func (m *Minitel) sendAndClearBuffer() error {
	err := m.sendBuffer()

	var retry int
	for err != nil && retry < MaxRetry {
		retry++
		err = m.sendBuffer()
		time.Sleep(10 * time.Millisecond)
	}

	if err == nil {
		m.clearBuffer()
	}
	return err
}

func (m *Minitel) MoveCursorXY(x, y int) error {
	inBound, err := IsPosInBounds(x, y, m.resolution)
	if err != nil {
		return fmt.Errorf("unable to move cursor: %w", err)
	}
	if !inBound {
		return fmt.Errorf("unable to move cursor: values (x=%d,y=%d) out of bound", x, y)
	}

	m.buffer = GetMoveCursorXY(m.buffer, x, y)
	return m.sendAndClearBuffer()
}

func (m *Minitel) MoveCursorLeft(n int) error {
	m.buffer = GetMoveCursorLeft(m.buffer, n)
	return m.sendAndClearBuffer()
}

func (m *Minitel) MoveCursorRight(n int) error {
	m.buffer = GetMoveCursorRight(m.buffer, n)
	return m.sendAndClearBuffer()
}

func (m *Minitel) MoveCursorDown(n int) error {
	m.buffer = GetMoveCursorDown(m.buffer, n)
	return m.sendAndClearBuffer()
}

func (m *Minitel) MoveCursorUp(n int) error {
	m.buffer = GetMoveCursorUp(m.buffer, n)
	return m.sendAndClearBuffer()
}

func (m *Minitel) MoveCursorReturn(n int) error {
	m.buffer = GetMoveCursorReturn(m.buffer, n)
	return m.sendAndClearBuffer()
}

func (m *Minitel) CleanScreen() error {
	m.buffer = GetCleanScreen(m.buffer)
	return m.sendAndClearBuffer()
}

func (m *Minitel) CleanScreenFromCursor() error {
	m.buffer = GetCleanScreenFromCursor(m.buffer)
	return m.sendAndClearBuffer()
}

func (m *Minitel) CleanScreenToCursor() error {
	m.buffer = GetCleanScreenToCursor(m.buffer)
	return m.sendAndClearBuffer()
}

func (m *Minitel) CleanLine() error {
	m.buffer = GetCleanLine(m.buffer)
	return m.sendAndClearBuffer()
}

func (m *Minitel) CleanLineFromCursor() error {
	m.buffer = GetCleanLineFromCursor(m.buffer)
	return m.sendAndClearBuffer()
}

func (m *Minitel) CleanLineToCursor() error {
	m.buffer = GetCleanLineToCursor(m.buffer)
	return m.sendAndClearBuffer()
}

func (m *Minitel) PrintMessage(msg string) error {
	var err error
	if m.buffer, err = GetMessage(m.buffer, msg); err != nil {
		return fmt.Errorf("unable to send message: %w", err)
	}
	return m.sendAndClearBuffer()
}
