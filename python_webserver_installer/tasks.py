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
import json
from cloudify.decorators import operation


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
def configure(ctx, **kwargs):
    ctx.logger.info(
        'Creating HTTP server root directory at: {0}'.format(
            get_webserver_root()))
    os.system('mkdir -p {0}'.format(get_webserver_root()))
    html = """
<html>
    <header>
        <title>Cloudify Hello World</title>
    </header>
<body>
    <h1>Hello, World!</h1>
    <p>
        blueprint_id = {0}<br/>
        deployment_id = {1}<br/>
        node_name = {2}<br/>
        node_id = {3}
    </p>
</body>
</html>
    """.format(ctx.blueprint_id, ctx.deployment_id, ctx.node_name, ctx.node_id)
    html_file = os.path.join(get_webserver_root(), 'index.html')
    ctx.logger.info('Creating index.html file at: {0}'.format(html_file))
    if not os.path.exists(html_file):
        with open(html_file, 'w') as f:
            f.write(html)


@operation
def start(ctx, port=8080, **kwargs):
    command = 'cd {0}; nohup python -m SimpleHTTPServer {1} &'.format(
        get_webserver_root(), port)
    ctx.logger.info('Starting HTTP server using: {0}'.format(command))
    os.system(command)
    verify_http_server(port)
    ctx.set_started()
    if 'ips' in ctx.capabilities:
        ips = json.dumps(ctx.capabilities['ips'])
        ctx.logger.info('HTTP Server IPs: {0}'.format(ips))
