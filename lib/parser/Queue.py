# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2020 Northwave B.V. (www.northwave-security.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import queue
import threading

from lib.parser.Consumer import Consumer


class Queue:

    items = queue.Queue()

    results = set()

    finishing = False

    finished = False

    consumers = []

    consumer_threads = []

    consumer_amount = 10

    def __init__(self, consumer_amount=5):
        self.consumer_amount = consumer_amount

    def start(self):
        self.create_consumers()

        for consumer in self.consumers:
            consumer_thread = threading.Thread(target=consumer.run)
            self.consumer_threads.append(consumer_thread)
            consumer_thread.start()

    def join(self):
        # Wait until queue is empty
        self.items.join()

        # Signal consumers to stop
        self.finishing = True

        # Wait until consumers stopped
        for consumer_thread in self.consumer_threads:
            consumer_thread.join()

        # We're finished
        self.finished = True

    def create_consumers(self):
        for i in range(0, self.consumer_amount):
            self.consumers.append(Consumer(i, self))
