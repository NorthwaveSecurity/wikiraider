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

import os
import re
import bz2
import json
import requests
import colorlog
import tqdm
import xml.etree.cElementTree


class ActionParse:
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
        archive_urls = self.get_archive_urls()

        for archive_url in archive_urls:
            archive_name = archive_url['key']
            archive_size = archive_url['size']
            archive_url = archive_url['url']

            path = os.path.dirname(os.path.abspath(__file__))
            archive_file = '{}/../../tmp/{}'.format(path, archive_name)

            if os.path.exists(archive_file) and os.path.getsize(archive_file) == archive_size:
                colorlog.getLogger().info('Using cached XML file on disk: {}'.format(archive_name))
            else:
                self.download_archive(archive_size, archive_url, archive_file)

            xml_file = self.extract_archive(archive_size, archive_name, archive_file)

            for event, element in xml.etree.cElementTree.iterparse(open(xml_file, 'r')):
                if element.tag.endswith('page'):
                    title = element.find('.//{http://www.mediawiki.org/xml/export-0.10/}title')
                    revision = element.find('.//{http://www.mediawiki.org/xml/export-0.10/}revision')
                    text = revision.find('.//{http://www.mediawiki.org/xml/export-0.10/}text')

                    element.clear()

                    self.process_page(title, text)
                    break

    def process_page(self, title, text):
        print('Processing:', title)
        pass

    def get_archive_urls(self):
        json_dumpstatus_url = '{}/dumpstatus.json'.format(self.args.url.strip('/'))
        response_object = requests.get(json_dumpstatus_url)
        response = json.loads(response_object.text)

        if not 'articlesdump' in response['jobs']:
            raise Exception('Could not find `articlesdump` on {}'.format(json_dumpstatus_url))

        article_object = response['jobs']['articlesdump']
        search_pattern = re.compile(r'^.*.xml.*.bz2$')

        results = []

        for key, value in article_object['files'].items():
            colorlog.getLogger().info('Investigating file {}'.format(key))

            if search_pattern.match(key):
                colorlog.getLogger().success('Identified XML file {}'.format(key))

                results.append({
                    'key': key,
                    'size': value['size'],
                    'url': '{}/{}'.format(self.args.url.strip('/'), key)
                })

        return results

    def download_archive(self, size: int, url: str, archive_file: str):
        colorlog.getLogger().info('Downloading {}'.format(url))

        with tqdm.tqdm(total=size) as progress:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(archive_file, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                            progress.update(8192)

        colorlog.getLogger().success('Download finished')

        return archive_file

    def extract_archive(self, size: int, archive_name: str, archive_file: str):
        colorlog.getLogger().info('Extracting {}'.format(archive_name))

        with tqdm.tqdm(total=size) as progress:
            with open(archive_file[0:-4], 'wb') as new_file:
                with open(archive_file, 'rb') as file:
                    decompressor = bz2.BZ2Decompressor()
                    for data in iter(lambda: file.read(100 * 1024), b''):
                        new_file.write(decompressor.decompress(data))
                        progress.update(100 * 1024)

        colorlog.getLogger().success('Extraction finished')
        return archive_file[0:-4]
