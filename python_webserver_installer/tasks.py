#/*******************************************************************************
# * Copyright (c) 2013 GigaSpaces Technologies Ltd. All rights reserved
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *       http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.
# *******************************************************************************/

"""
A celery task for starting a simple http server using a python command.
"""

import time
import urllib2
import os

from celery import task

from cosmo.events import send_event


@task
def install(**kwargs):
    pass


@task
def start(__cloudify_id, port=8080, **kwargs):
    os.system("nohup python -m SimpleHTTPServer {0} &".format(port))

    # verify http server is up
    for attempt in range(10):
        try:
            response = urllib2.urlopen("http://localhost:{0}".format(port))
            response.read()
            break
        except BaseException:
            time.sleep(1)
    else:
        raise RuntimeError("failed to start python http server")
    send_event(__cloudify_id, "10.0.0.5", "webserver status", "state", "running")