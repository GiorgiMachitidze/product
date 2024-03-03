import threading
import time
import requests

import json

def req(link):
    s = requests.get(link)
    return s.json()


class CustomThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(CustomThread, self).__init__(*args, **kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        super(CustomThread, self).join()
        return self._return
variables = []
links = []
for i in range(1, 101):
    variables.append(f"i{i}")
    links.append(f"i{i}")
for i in range(1, 101):
    variables[i-1] = CustomThread(target = req, args = (f"https://dummyjson.com/products/{i}",))
    variables[i-1].start()
for i in range(1, 101):
    links[i-1] = variables[i-1].join()
print(time.perf_counter())
output_file = 'products.json'
with open(output_file, 'w') as f:
    f.write("[")
    for result in links:
        json.dump(result, f)
        if result != links[99]:
            f.write(",")
        f.write('\n')
    f.write("]")


