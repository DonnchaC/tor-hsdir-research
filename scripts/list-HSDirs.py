"""
Parses the cached consensus of a running Tor instance from file
and outputs the hidden service directories as a CSV file. Useful
for determining the responsible hidden services directories at
a particular time

- Donncha O' Cearbhaill - donncha@totalimpact.ie
  PGP: 0xAEC10762
"""
from stem.descriptor import parse_file, DocumentHandler
from stem.descriptor.router_status_entry import RouterStatusEntryV3, _decode_fingerprint
import base64

with open('/var/lib/tor/cached-consensus', 'rb') as consensus_file:
  # Processes the routers as we read them in. The routers refer to a document
  # with an unset 'routers' attribute.
  for router in parse_file(consensus_file, 'network-status-consensus-3 1.0', document_handler = DocumentHandler.ENTRIES):
    if "HSDir" in router.flags:
      fingerprint_base32 =  base64.b32encode(router.fingerprint.decode("hex"))
      print "'%s','%s','%s','%s'" % (fingerprint_base32, router.nickname, router.fingerprint, router.address)

