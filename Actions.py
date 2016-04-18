import queue as q

# This class handles actions from the mainloop

class _Action:
    def __init__(self, command, params):
        self.command = command
        self.params = params

    def do(self, network):
        network.send()

class check(_Action):
    def __init__(self, command, params):
        _Action.__init__(command, params)
        
        
        

class ActionHandler:
    def __init__(self, network):
        pending = q.Queue()  # Array of Actions to send over network
        
    def executePending(self):
        pass
