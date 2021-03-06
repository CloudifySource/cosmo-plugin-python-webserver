########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

__author__ = 'elip'

import shutil
import unittest
from os import path
from python_webserver_installer import tasks
from cloudify.mocks import MockCloudifyContext


class WebserverInstallerTestCase(unittest.TestCase):

    def setUp(self):
        def dummy(*args, **kwargs):
            return None
        tasks.get_ip = dummy
        tasks.set_node_started = dummy

    def test_http_server(self):
        context = MockCloudifyContext(
            node_id='id',
            properties={'image_path': 'images/mock-image.png'})
        root_dir = tasks.get_webserver_root()
        if path.exists(root_dir):
            shutil.rmtree(root_dir)
        tasks.configure(context)
        html_file = path.join(root_dir, 'index.html')
        self.assertTrue(path.exists(html_file))
        tasks.start(context, port=8000)
        tasks.verify_http_server(port=8000)
        tasks.stop(context)
