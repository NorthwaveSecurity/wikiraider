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

import re


class ParserHelper:
    """The Parser class contains helper functions for parsing Wikipedia elements to wordlists (hashsets).

    Attributes:
        title_delimiters (str): A regex with characters that do not belong to words. These characters are used to split the title into words.
        text_delimiters (str): A regex with characters that do not belong to words. These characters are used to split the text into words.

    """

    title_delimiters = r'''\\\w|\ |\,|\.|\ |\:|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\_|\=|\=|\-|\`|\~|\[|\]|\{|\}|\;|\:|\"|\'|\/|\?|\.|\,|\>|\<|\|'''

    text_delimiters = r'''\\\w|\ |\,|\.|\ |\:|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\_|\=|\=|\-|\`|\~|\[|\]|\{|\}|\;|\:|\"|\'|\/|\?|\.|\,|\>|\<|\|'''

    @staticmethod
    def get_words_from_title(title):
        """Convert the given title into a wordlist.

        Args:
            title (str): The title of a Wikipedia page.

        Returns:
            set: The words that were extracted from the title.

        Note:
            This function currently only supports words that comply with the regex `[A-zÀ-ú]+`.

        """

        results = set()

        title = re.sub(ParserHelper.title_delimiters, ' ', title)
        results.update(re.findall(r'[A-zÀ-ú]+', title))

        return results

    @staticmethod
    def get_words_from_text(text):
        """Convert the given text into a wordlist.

        Args:
            text (str): The contennt of a Wikipedia page.

        Returns:
            set: The words that were extracted from the content.

        Note:
            This function currently only supports words that comply with the regex `[A-zÀ-ú]+`.

        """

        results = set()

        text = re.sub(ParserHelper.text_delimiters, ' ', text)
        results.update(re.findall(r'[A-zÀ-ú]+', text))

        return results
