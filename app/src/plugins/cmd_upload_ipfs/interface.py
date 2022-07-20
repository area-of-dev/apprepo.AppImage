# Copyright 2020 Alex Woroschilow (alex.woroschilow@gmail.com)
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

import hexdi

from modules.cmd import console


@console.task(name=['upload-ipfs'], description="upload a new version of the AppImage using IPFS_CID")
@hexdi.inject('config', 'apprepo', 'console.application')
def main(options=None, args=None, config=None, apprepo=None, console=None):
    """

    :param options:
    :param args:
    :param config:
    :param apprepo:
    :param console:
    :param hasher:
    :return:
    """
    if not options.version_token: raise Exception('Version token is empty')
    if not options.version_name: raise Exception('Version name is empty')
    if not options.version_hash: raise Exception('Version hash is empty')
    if not options.version_description: raise Exception('Unknown description')
    if not options.version_ipfs_cid: raise Exception('Unknown version_ipfs_cid')

    package_version = apprepo.package_ipfs_cid_new(
        config.get('user.token', None),

        options.version_token,
        options.version_name,
        options.version_description,
        options.version_hash,

        options.version_ipfs_cid,
        options.version_ipfs_gateway
    )

    if not package_version:
        raise Exception('{} package version not found'.format(
            options.version_token
        ))

    yield console.green("[done] {}: {}...".format(
        options.version_name,
        options.version_ipfs_cid
    ))
