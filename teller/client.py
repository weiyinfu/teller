import sys

import requests

from teller import config

args = " ".join(sys.argv[1:])
resp = requests.get(f"http://localhost:{config.port}", params={"content": args})
if resp.text:
    print(resp.text)
