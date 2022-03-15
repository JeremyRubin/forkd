#!/usr/bin/python3
# Copyright 2022 Jeremy Rubin

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
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

import http
import http.client
import sys
import base64
import time
import json
if __name__ == "__main__":
    [host, port, user, password, target] = sys.argv[1:]
    stats = lambda n: json.dumps({"jsonrpc": "1.0", "id": f"forkd{n}", "method": "getdeploymentinfo", "params": []})
    invalidate = lambda n, h: json.dumps({"jsonrpc": "1.0", "id": f"forkd-invalidate-{n}", "method": "invalidateblock", "params": [h]})
    cred = bytes(user + ':' + password, 'utf-8')
    auth = b'Basic ' + base64.b64encode(cred)
    count = 0
    def make_request(r):
        conn = http.client.HTTPConnection(host, port, timeout=10)
        conn.request('POST', "", r,
                    {'Host': "",
                     'User-Agent': "forkd",
                     'Authorization': auth,
                     'Content-type': 'application/json'})
        conn.sock.settimeout(30)
        resp = json.loads(conn.getresponse().read().decode('utf8'))['result']
        return resp

    while True:
        count += 1
        resp = make_request(stats(count))
        print(resp)
        block = resp['hash']
        deployments = resp['deployments']
        do_invalidate = False
        if target in deployments:
            print(deployments[target])
            if 'statistics' in deployments[target]:
                deploy = deployments[target]['statistics']
                if deploy.count >= deploy.threshold:
                    do_invalidate = True
            elif deployments[target]['active']:
                do_invalidate = True

        if do_invalidate:
            print(f"Invalidating block {block}")
            make_request(invalidate(count, block))
        else:
            print("Sleeping")
            time.sleep(10)
