package main

import (
	"flag"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/websocket"
)

var addr = flag.String("addr", "localhost:8080", "http service address")

var upgrader = websocket.Upgrader{CheckOrigin: func(r *http.Request) bool { return true }} // use default options

func server(w http.ResponseWriter, r *http.Request) {
	m := Minitel{
		resolution: ResolutionSimple,
		fontSize:   GrandeurNormale,
	}

	c, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Print("upgrade:", err)
		return
	}
	defer c.Close()

	for {
		msg := m.GetMessage("BONJOUR! ")
		log.Println("sent: ", msg)
		err = c.WriteMessage(websocket.TextMessage, []byte{27,
			219,
			178,
			202,
			27,
			219,
			177,
			187,
			177,
			72,
			27,
			204,
			27,
			71,
			27,
			92,
			27,
			219,
			180,
			187,
			177,
			53,
			72,
			46,
			46,
		})
		if err != nil {
			log.Println("write:", err)
			break
		}
		time.Sleep(time.Second)
	}
}

func main() {
	flag.Parse()
	log.SetFlags(0)
	http.HandleFunc("/", server)
	log.Fatal(http.ListenAndServe(*addr, nil))
}
