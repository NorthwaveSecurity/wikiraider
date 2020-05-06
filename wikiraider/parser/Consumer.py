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

import time
import colorlog
import traceback

from wikiraider.helpers.ParserHelper import ParserHelper


class Consumer:
    """A consumer (launched as thread) that will parse Wikipedia items on the queue."""

    def __init__(self, alias, queue):
        """Convert the given title into a wordlist.

        Args:
            alias (int): The identifier of this thread.
            queue (:class:`wikiraider.parser.Queue`): The queue to get items from.

        """

        self.alias = alias
        self.queue = queue

    def __str__(self):
        """Get a string representation of this consumer (containing its alias).

        Returns:
            str: A string representing the consumer.

        """

        return 'Consumer #{}'.format(self.alias)

    def run(self):
        """Start the consumer and parse items on the queue in a while loop.

        Note:
            This function will return (thread will stop) if there are no more items on the queue, and if no more items are added to the queue.

        """

        while not self.queue.finishing:
            while not self.queue.items.empty():
                try:
                    (title, text) = self.queue.items.get(block=True, timeout=1)

                    try:
                        self.on_page(title, text)
                    except Exception as e:
                        colorlog.getLogger().error('Exception occurred while parsing page. {}'.format(str(e)))
                        traceback.print_exc()

                    self.queue.items.task_done()
                except:
                    colorlog.getLogger().info('{} is idle. Will auto start if new items are on the queue.'.format(str(self)))

            time.sleep(1)

    def on_page(self, title, text):
        """Callback, called when the consumer got a Wikipedia page of the queue.

        Args:
            title (str): The title of the Wikipedia page.
            text (str): The content of the Wikipedia page.

        Note:
            This function updates the queue results with the words that were found on the page or in the title. The queue results type is a set, and thus thread safe.

        """

        if type(title.text) is str:
            self.queue.results.update(
                ParserHelper.get_words_from_title(title.text)
            )

        if type(text.text) is str:
            self.queue.results.update(
                ParserHelper.get_words_from_text(text.text)
            )
