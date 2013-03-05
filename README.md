tor
===

Modified version of Tor for investigating HidServ DHT.

Currently just trying to understand the code, should log and output at four points:
* When server receives a v0 hidden service descriptor - rend_cache_store() - rendcommon.c - Done
* When server receives a v2 hidden service descriptor - rend_cache_store_v2_desc_as_dir() - rendcommon.c - Done
* When directory server receives request for a v0 hidden service descriptor - directory.c Line 3273 - Done
* When directory server receives request for a v2 hidden service descriptor - directory.c - Line 3245 - Done

Looks like only v2 is need. v0 service descriptors were only published to the the original hs directory authorities. 
https://gitweb.torproject.org/torspec.git/blob/HEAD:/rend-spec.txt
