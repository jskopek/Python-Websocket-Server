import time
import re
import struct
import socket
import hashlib

address = "127.0.0.1"
port = 2222

class Server:
    def __init__( self, address, port, connections=1000 ):
        server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

        connected = False
        while not connected:
            try:
                server.bind( (address, port) )
            except socket.error:
                print "Error initialing server on %s:%s. Will try again in 1s"%(address, port)
                time.sleep(1)
            else:
                print "Initialized server on %s:%s"%(address, port)
                connected = True

        server.listen( connections )

        while True:
            req, details = server.accept()
            conn = Connection( req )

class Connection:
    def __init__( self, conn ):
        print( "Connecting", conn )
        data = conn.recv( 1024 )

        resp = self.prepare_handshake( data )
        conn.send( resp )


    def handshake( self, data ):
        origin = re.compile("Origin: (.*)\r\n").findall(data)[0]
        host = re.compile("Host: (.*)\r\n").findall(data)[0]
        key1 = re.compile("Sec-WebSocket-Key1: (.*)\r\n").findall(data)[0]
        key2 = re.compile("Sec-WebSocket-Key2: (.*)\r\n").findall(data)[0]
        body = data[ len(data) - 8: ]

        return [origin, host, key1, key2, body]

    def prepare_handshake( self, data ):
        data = self.handshake( data )

        key1 = data[2]
        key1_nums = re.sub("[^\d]", "", key1)
        key1_num_spaces = len( re.sub("[^\s]", "", key1) )
        key1_result = int( int( key1_nums ) / key1_num_spaces )

        key2 = data[3]
        key2_nums = re.sub("[^\d]", "", key2)
        key2_num_spaces = len( re.sub("[^\s]", "", key2) )
        key2_result = int( int( key2_nums ) / key2_num_spaces )

        merge = "%s%s%s"%(key1_result, key2_result, data[4])
        merge = struct.pack(">II8s", key1_result, key2_result, data[4])
        hash = hashlib.md5(merge).digest()

        return ("HTTP/1.1 101 WebSocket Protocol Handshake\r\n"
"Upgrade: WebSocket\r\n"
"Connection: Upgrade\r\n"
"Sec-WebSocket-Origin: %s\r\n"
"Sec-WebSocket-Location: ws://%s/\r\n"
"Sec-WebSocket-Protocol: sample\r\n"
"\r\n"
"%s") % ( data[0], data[1], hash )


if __name__ == "__main__":
    server = Server( address, port )
