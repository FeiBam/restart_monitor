

class EventEmitter:
    def __init__(self):
        self.events = {}

    def on(self, event, listener):
        if event not in self.events:
            self.events[event] = []
        self.events[event].append(listener)

    def emit(self, event, *args, **kwargs):
        if event in self.events:
            for listener in self.events[event]:
                listener(*args, **kwargs)