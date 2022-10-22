package minigo

func BitReadAt(b byte, i int) bool {
	return b&(1<<i) == 1
}

func IsByteEven(b byte) bool {
	even := false
	for i := 0; i < 7; i++ {
		if BitReadAt(b, i) {
			even = !even
		}
	}

	return even
}

func BitWriteAt(b byte, i int, value bool) byte {
	if value {
		return b | 1<<i
	} else {
		return b &^ 1 << i
	}
}

func SetByteParity(b byte) byte {
	return BitWriteAt(b, 7, IsByteEven(b))
}

func CheckByteParity(b byte) byte {
	if IsByteEven(b) && BitReadAt(b, 7) {
		return BitWriteAt(b, 7, false)
	} else {
		return 0xFF
	}
}

func GetProCode(i int) []byte {
	buf := []byte{SetByteParity(Esc)}
	switch i {
	case 1:
		buf = append(buf, SetByteParity(0x39))
	case 2:
		buf = append(buf, SetByteParity(0x3A))
	case 3:
		buf = append(buf, SetByteParity(0x3B))
	}
}

func GetPCode(i int) []byte {
	var buf []byte
	if i < 10 {
		buf = append(buf, SetByteParity(0x30+byte(i)))
	} else {
		buf = append(buf, SetByteParity(0x30+byte(i/10)))
		buf = append(buf, SetByteParity(0x30+byte(i%10)))
	}
}
