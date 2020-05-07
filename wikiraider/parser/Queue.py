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

from wikiraider.parser.Consumer import Consumer


class Queue:
    """The Wikipedia pages queue. Used to track items (title/content) and the consumers parsing these items.

    Attributes:
        items (:class:`queue.Queue`): The actual native Python queue in use.
        results (set): The words result (hash)set. This is thread safe.
        finishing (bool): True when all items are added to the queue, but consumers are still busy processing them.
        finished (bool): True when the queue has finished (no more items are added and the items are empty).
        consumers (list): A list of created consumer classes.
        consumer_threads (list): A list of created consumers threads, this reference can be used to join them later.
        consumer_amount (int): The amount of consumers (threads) to use.

    """

    items = queue.Queue()

    results = set()

    finishing = False

    finished = False

    consumers = []

    consumer_threads = []

    consumer_amount = None

    def __init__(self, consumer_amount=5):
        """Initialize the queue in idle state.

        Args:
            consumer_amount (int): The amount of consumers (threads) to use.

        """

        self.consumer_amount = consumer_amount

    def start(self):
        """Start all consumers and make them parse items on the queue."""

        self.create_consumers()

        for consumer in self.consumers:
            consumer_thread = threading.Thread(target=consumer.run)
            consumer_thread.start()

            self.consumer_threads.append(consumer_thread)

    def create_consumers(self):
        """Create all the consumer classes (not yet the threads).

        Note:
            Consumers are created using an alias (int) to distinguish them from each other.

        """

        for i in range(0, self.consumer_amount):
            self.consumers.append(Consumer(i, self))

    def join(self):
        """Wait for all consumers to finish.

        Note:
            First join the items (:class:`queue.Queue`) to make sure all items have been parsed. Then join all the threads.

        """

        # Wait until queue is empty
        self.items.join()

        # Signal consumers to stop
        self.finishing = True

        # Wait until consumers stopped
        for consumer_thread in self.consumer_threads:
            consumer_thread.join()

        # We're finished
        self.finished = True
