package main

import (
	"fmt"
	"io"
	"net"
)

type Driver interface {
	popHead() (byte, error)

	Recv() (byte, error)
	Readable() (bool, error)
	Send(msg []byte) (int, error)
}

type TCPDriver struct {
	conn       net.Conn
	recvBufLen int
	recvBufPos int
	recvBuf    []byte
}

func NewTCPDriver(conn net.Conn) *TCPDriver {
	return &TCPDriver{
		conn:       conn,
		recvBufLen: 0,
		recvBufPos: 0,
		recvBuf:    make([]byte, 1024),
	}
}

func (t *TCPDriver) popHead() (byte, error) {
	if t.recvBufLen == 0 {
		return 0, io.EOF
	}

	if t.recvBufPos < t.recvBufLen {
		b := t.recvBuf[t.recvBufPos]
		t.recvBufPos++
		return b, nil
	} else {
		t.recvBufPos, t.recvBufLen = 0, 0
		return 0, io.EOF
	}
}

func (t *TCPDriver) Recv() (byte, error) {
	if b, err := t.popHead(); err == nil {
		return b, nil
	} else if err != io.EOF {
		return 0, fmt.Errorf("unable to popHead: %w", err)
	}

	var err error
	t.recvBuf = make([]byte, 1024)
	t.recvBufLen, err = t.conn.Read(t.recvBuf)
	if err != nil {
		t.recvBufLen, t.recvBufPos = 0, 0
		return 0, fmt.Errorf("unable to read from TCP: %w", err)
	}

	if b, err := t.popHead(); err == nil {
		return b, nil
	} else if err != io.EOF {
		return 0, fmt.Errorf("unable to popHead: %w", err)
	} else {
		return 0, fmt.Errorf("buffer EOF: %w", err)
	}
}

func (t *TCPDriver) Readable() (bool, error) {
	return true, nil
}

func (t *TCPDriver) Send(buf []byte) (int, error) {
	return t.conn.Write(buf)
}
