package main

type Driver interface {
	Recv() ([]byte, error)
	Readable() (bool, error)
	Send(msg []byte) error
}
