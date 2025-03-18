import socketserver

from tcpHandler import TcpHandler

class ErpServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, address, handler):
        socketserver.ThreadingMixIn.__init__(self)
        socketserver.TCPServer.__init__(self, address, handler)

    def run(self):
        try:
            print("서버 실행")
            self.serve_forever()
        except KeyboardInterrupt:
            print("서버 종료")
            self.shutdown()
            self.server_close()

if __name__ == "__main__":
    HOST = "localhost"
    # HOST = "192.168.0.29"
    PORT = 12345
    server = ErpServer((HOST, PORT), TcpHandler)
    server.run()