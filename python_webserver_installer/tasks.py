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

"""
Cloudify plugin for running a Python simple HTTP server.

Operations:
    configure: Creates an index.html file.
    start: Starts the server
"""

import time
import urllib2
import os
import tempfile
from cloudify.decorators import operation
from cloudify.notifications import send_reachable as send_riemann_reachable
from cloudify.utils import get_local_ip


get_ip = get_local_ip
send_reachable = send_riemann_reachable


def get_webserver_root():
    return os.path.join(tempfile.gettempdir(), 'python-simple-http-webserver')


def verify_http_server(port=8080):
    for attempt in range(15):
        try:
            response = urllib2.urlopen("http://localhost:{0}".format(port))
            response.read()
            break
        except BaseException:
            time.sleep(1)
    else:
        raise RuntimeError("failed to start python http server")


@operation
def configure(__cloudify_id, **kwargs):
    os.system('mkdir -p {0}'.format(get_webserver_root()))
    html = """
<html>
    <header>
        <title>Cloudify Hello World</title>
    </header>
<body>
    <h1>Hello, World!</h1>
    <p>node_id = {0}</p>
</body>
</html>
    """.format(__cloudify_id)
    html_file = os.path.join(get_webserver_root(), 'index.html')
    if not os.path.exists(html_file):
        with open(html_file, 'w') as f:
            f.write(html)


@operation
def start(__cloudify_id, port=8080, **kwargs):
    os.system("cd {0}; nohup python -m SimpleHTTPServer {1} &".format(get_webserver_root(), port))
    verify_http_server(port)
    send_reachable(__cloudify_id, get_ip())

