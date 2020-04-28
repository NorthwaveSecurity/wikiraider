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

import bs4
import requests
import colorlog

class ActionList:
    """The Package class contains all the package related information (like the version number).

    Attributes:
        __name (str): Cached package name.
        __description (str): Cached package description.
        __alias (str): Cached package alias.
        __version (str): Cached package version number (if initialized).

    """

    def __init__(self, args):
        self.args = args

    def run(self):
        search_info = 'matching `{}`'.format(self.args.search) if self.args.search else ''
        colorlog.getLogger().info('Listing all Wikimedia dumps {}...'.format(search_info))

        dumps = self.get_dumps()

        for dump in dumps:
            colorlog.getLogger().success('Name: {}, URL: {}'.format(dump['name'], dump['url']))

    def get_dumps(self):
        response = requests.get('{}/backup-index.html'.format(self.args.cdn))
        soup = bs4.BeautifulSoup(response.text, features="html.parser")

        dumps = []

        for dump_complete in soup.find_all('span'):
            if 'done' not in dump_complete['class']:
                # Span is not a dump or dump is not complete
                continue

            if not dump_complete.string == 'Dump complete':
                # Dump is not complete
                continue

            datetime_array = dump_complete.parent.text.split(' ')
            date = datetime_array[0]
            time = datetime_array[1]
            link = dump_complete.parent.find('a')

            if not link:
                # Dump may be private
                continue

            if not link.text.endswith('wiki') or len(link.text) > 7:
                # Not a normal wiki (probably wiktionary or something)
                continue

            if self.args.search:
                haystack = link.text[0:-4].lower().strip()
                needle = self.args.search.lower().strip()

                if haystack not in needle or needle not in haystack:
                    # Not the correct search result
                    continue

            dumps.append({
                'url': '{}/{}'.format(self.args.cdn, link['href']),
                'alias': link.text,
                'name': link.text[0:-4],
                'date': date,
                'time': time
            })

        return dumps
