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
        print('Key data match')
        return data1
    else:
        print('Key data did not match, try again')
    # record key data for both keys
    while True:
        print(f'Press the key named "{name}".')
        data1 = receive_and_decode()
        print('Press the same key again to verify')
        data2 = receive_and_decode()
        if data1 == data2:
            return data1
        else :
          data1[0]['alt_hash'] = data2[0]['hash']
          data1[0]['alt_coding'] = data2[0]['coding']
          return data1

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
