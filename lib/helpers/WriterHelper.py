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
import pathlib
import datetime

class WriterHelper:

    @staticmethod
    def make_directory(wiki_name):
        path = './dist/{}'.format(wiki_name)
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def get_file_path(wiki_name):
        today = datetime.datetime.now()
        path = './dist/{}/{}-{}.txt'.format(wiki_name, wiki_name, today.strftime('%Y-%m-%d'))
        return path

    @staticmethod
    def write_to_txt(wiki_name, words):
        WriterHelper.make_directory(wiki_name)
        path = WriterHelper.get_file_path(wiki_name)

        with open(path, 'w') as outfile:
            outfile.write('\n'.join(words))
