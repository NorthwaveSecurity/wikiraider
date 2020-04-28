class Producer:

    def __init__(self, queue, file):
        self.queue = queue
        self.file = file

    def run(self):
        print('Producer running with file {}'.format(self.file))

        for i in range(0, 5):
        	self.queue.put((self.file, i))