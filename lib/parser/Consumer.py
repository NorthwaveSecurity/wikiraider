import time


class Consumer:
    def __init__(self, alias, queue):
        self.alias = alias
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            item = self.queue.get()
            print(self.alias, item)
            self.queue.task_done()
