from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
import win32com.client, os

qinfo = win32com.client.Dispatch("MSMQ.MSMQQueueInfo")
q1info = win32com.client.Dispatch("MSMQ.MSMQQueueInfo")
computer_name = os.getenv('COMPUTERNAME')
qinfo.FormatName="direct=os:"+computer_name+"\\PRIVATE$\\123"
q1info.FormatName = "direct=os:"+computer_name+"\\PRIVATE$\\321"
rec_q = qinfo.Open(2, 0)
send_q = q1info.Open(1, 0)

class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        msg = win32com.client.Dispatch("MSMQ.MSMQMessage")
        msg.Label = ""
        msg.Body = payload
        msg.Send(send_q)
        msg = rec_q.Receive()
        self.sendMessage(msg, False)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    # note to self: if using putChild, the child must be bytes...

    reactor.listenTCP(9000, factory)
    reactor.run()