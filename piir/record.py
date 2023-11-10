import json, os, sys
from .io import receive
from .decode import decode
from .util import hexify
from .prettify import prettify
from .remote import Remote

glitch = 100
timeout = 100
tolerance = 0.2
gap = 15, 
pulses = 10
carrier = 38
gpio = 22

def do_receive():
    return receive(gpio, glitch=glitch, timeout=timeout)

def receive_and_decode():
    while True:
        data = decode(do_receive())
        if data:
            return data

def record_key(name):
    print(f'Press the key named "{name}".')
    data1 = receive_and_decode()
    print('Press the same key again to verify.')
    data2 = receive_and_decode()
    if data2 == data1:
        return data2
    while True:
        print('Press the same key again to verify.')
        data3 = receive_and_decode()
        if data3 == data1 or data3 == data2:
            return data3
        data1 = data2
        data2 = data3

def record(file):
    keys = {}
    if os.path.exists(file):
        print(f'Loading "{file}"...')
        remote = Remote(file, None)
        keys = remote.unprettify()
        print('The following buttons have been recorded:')
        for key in keys:
            print(key,':',keys[key][0]['coding'],keys[key][0]['hash'])
    while True:
        name = input('Name of the key (blank to finish): ')
        if not name:
            break
        keys[name] = record_key(name)
    data = prettify(keys, carrier=int(round(carrier * 1000)))
    json.dump(data, open(file, 'w', encoding='utf8'), indent=2)
    print(f'Saved to "{file}".')
