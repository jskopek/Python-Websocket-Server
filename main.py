import socket

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
                print "Error initialing server on %s:%s. Trying again in 1s"%(address, port)
                time.sleep(1)
            else:
                print "Initialized server on %s:%s. Trying again in 1s"%(address, port)
                connected = True

        server.listen( connections )

        while True:
            req, details = server.accept()
            conn = Connection( req )

class Connection:
    def __init__( self, conn ):
        print( "Connecting", conn )

if __name__ == "__main__":
    server = Server( address, port )
