# -*- coding: utf-8 -*-
# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inject


@inject.params(config='config', apprepo='apprepo', logger='logger')
def main(options=None, args=None, config=None, apprepo=None, logger=None):
    from bs4 import BeautifulSoup

    def strip_tags(html=None):
        if html is None:
            return None

        soup = BeautifulSoup(html, "html5lib")
        [x.extract() for x in soup.find_all('script')]
        [x.extract() for x in soup.find_all('style')]
        [x.extract() for x in soup.find_all('meta')]
        [x.extract() for x in soup.find_all('noscript')]
        [x.extract() for x in soup.find_all('iframe')]
        return soup.text

    string = ' '.join(args).strip('\'" ')
    if string is None or not len(string):
        raise Exception('search string can not be empty')

    for entity in apprepo.search(string):
        yield ("[match] {:>s} ({:>s}) - {:>s}".format(
            entity['name'] or 'Unknown',
            entity['version'] or 'Unknown',
            strip_tags(entity['description']) or 'Unknown'
        ))
    return 0
