from channels.generic.websocket import JsonWebsocketConsumer

class CanvasConsumer(JsonWebsocketConsumer):
    groups = ["broadcast"]

    def connect(self):
        self.accept()


        if self.scope['user'].is_authenticated:
            self.accept()
        else:
            self.close()


    def receive_json(self, content, **kwargs):

        if content['command'] == "CHAT":
            name = content['name']
            data = self.load_conversation_contact(name)
        else:
            data = {"success": False, "errors": "no such command"}
            self.send_json(data) # the error happens here


        # Called with either text_data or bytes_data for each frame
        # You can call:
        self.send(text_data="Hello world!")
        # Or, to send a binary frame:
        self.send(bytes_data="Hello world!")
        # Want to force-close the connection? Call:
        self.close()
        # Or add a custom WebSocket error code!
        self.close(code=4123)

    def disconnect(self, close_code):
        # Called when the socket closes
        pass