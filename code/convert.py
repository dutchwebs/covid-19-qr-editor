#!/usr/bin/env python

import sys
import zlib
import pprint

import PIL.Image
import pyzbar.pyzbar
import base45
import cbor2

# Load QR code image
data = pyzbar.pyzbar.decode(PIL.Image.open(sys.argv[1]))
qr_content = data[0].data.decode()
prepend = "HC1:"

print(qr_content)

# Decrypt QR content
b45data = qr_content.replace(prepend, "")
zlibdata = base45.b45decode(b45data)
cbordata = zlib.decompress(zlibdata)
decoded = cbor2.loads(cbordata)
editable_obj = cbor2.loads(decoded.value[2])

print("\n-----------\n")

# Before
print(editable_obj[-260][1])

# Edit content
editable_obj[-260][1]['dob'] = '1996-01-21' # date of birth
editable_obj[-260][1]['nam'] = {'fn': 'Achternaam', 'fnt': 'ACHTERNAAM', 'gn': 'Voornaam Tweede Derde', 'gnt': 'VOORNAAM<TWEEDE<DERDE'} # names

 # After
print(editable_obj[-260][1])

print("\n-----------\n")

# Encrypt QR content again
decoded.value[2] = cbor2.dumps(editable_obj)
encoded = cbor2.dumps(decoded)
compressed = zlib.compress(encoded)
new_qr_content = prepend + base45.b45encode(compressed).decode("utf-8")

print(new_qr_content)
