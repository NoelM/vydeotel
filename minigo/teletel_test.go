package main

import "testing"

func TestBitReadAt(t *testing.T) {
	var b byte = 0b01000001
	if BitReadAt(b, 0) != true {
		// looking for: 0b01000001
		//                       ^
		t.Fatal("wrong value extracted at pos 0")
	}
	if BitReadAt(b, 6) != true {
		// looking for: 0b01000001
		//                 ^
		t.Fatal("wrong value extracted at pos 6")
	}
	if BitReadAt(b, 7) != false {
		// looking for: 0b01000001
		//                ^
		t.Fatal("wrong value extracted at pos 7")
	}
}

func TestIsByteEven(t *testing.T) {
	var evenByte byte = 0b01000001
	if IsByteEven(evenByte) != true {
		t.Fatalf("wrong parity extracted for even-byte: %d", evenByte)
	}

	var oddByte byte = 0b01100001
	if IsByteEven(oddByte) != false {
		t.Fatalf("wrong parity extracted for odd-byte: %d", oddByte)
	}
}

func TestBitWriteAt(t *testing.T) {
	var originalByte byte = 0b01000001
	var expectedByte byte = 0b11000001
	if computed := BitWriteAt(originalByte, 7, true); computed != expectedByte {
		t.Fatalf("expected result: %b got %b", expectedByte, computed)
	}

	expectedByte = 0b01100001
	if computed := BitWriteAt(originalByte, 5, true); computed != expectedByte {
		t.Fatalf("expected result: %b got %b", expectedByte, computed)
	}

	expectedByte = 0b00000001
	if computed := BitWriteAt(originalByte, 6, false); computed != expectedByte {
		t.Fatalf("expected result: %b got %b", expectedByte, computed)
	}

	expectedByte = 0b01000000
	if computed := BitWriteAt(originalByte, 0, false); computed != expectedByte {
		t.Fatalf("expected result: %b got %b", expectedByte, computed)
	}
}

func TestGetByteWithParity(t *testing.T) {
	var originalByte byte = 0b01000001
	var expectedByte byte = 0b01000001
	if computed := GetByteWithParity(originalByte); computed != expectedByte {
		t.Fatalf("expected result: %b got %b", expectedByte, computed)
	}

	originalByte = 0b01100001
	expectedByte = 0b11100001
	if computed := GetByteWithParity(originalByte); computed != expectedByte {
		t.Fatalf("expected result: %b got %b", expectedByte, computed)
	}
}

func TestCheckByteParity(t *testing.T) {
	var goodParityByte byte = 0b01000001
	var goodParityRemoved byte = 0b01000001
	if computed, err := CheckByteParity(goodParityByte); computed != goodParityRemoved || err != nil {
		t.Fatalf("wrong parity check for %b, expected %b, computed %b, with error: %s", goodParityByte, goodParityRemoved, computed, err.Error())
	}

	var wrongParityByte byte = 0b11000001
	var wrongParityRemoved byte = 0
	if computed, err := CheckByteParity(wrongParityByte); computed != wrongParityRemoved || err == nil {
		t.Fatalf("wrong parity check for %b, expected %b, computed %b, with error: %s", goodParityByte, wrongParityRemoved, computed, err.Error())
	}
}

func TestCharMapping(t *testing.T) {
	c, err := GetChar('A')
	if err != nil {
		t.Fatalf("recived error: %s", err.Error())
	}
	if c != 0x41 {
		t.Fatalf("recieved %x instead of %x", c, 0x41)
	}
}
