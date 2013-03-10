# Tor Hidden Service (DHT) Research
===

Modified version of Tor for investigating HidServ DHT.

Currently just trying to understand the code, should log and output at four points:
* When server receives a v0 hidden service descriptor - rend_cache_store() - rendcommon.c - Done
* When server receives a v2 hidden service descriptor - rend_cache_store_v2_desc_as_dir() - rendcommon.c - Done
* When directory server receives request for a v0 hidden service descriptor - directory.c Line 3273 - Done
* When directory server receives request for a v2 hidden service descriptor - directory.c - Line 3245 - Done

Looks like only v2 is need. v0 service descriptors were only published to the the original hs directory authorities. 
https://gitweb.torproject.org/torspec.git/blob/HEAD:/rend-spec.txt

## Other Ideas

### Background
Tor hidden service desc_id's are deterministic and if there is no 'descriptor cookie' they can be determined 
by anybody for an arbitrary point in time. In fact this is required as this is the mechanism by which clients request
hidden service descriptors.

    descriptor-id = H(permanent-id | H(time-period | descriptor-cookie | replica))

*decriptor-cookie* is typically empty. *replica* is an integer, usual from 0-1 which indicated which set of 
responsible HidServ directories this descriptor is for and *permanent-id* is derived from the service public key.

    time-period = (current-time + permanent-id-byte * 86400 / 256) / 86400

The *time-period* changes approximatly every 24 hours.

The HidServ directory *identity_digest* should be before the *desc_id* in a descending lists of all HidServ directories

### 1. Statistical and Traffic Analysis of Tor Hidden Services
It should be possible to determine more than 24 hours in advanced what a public hidden service desc_id will be. 
It should then be trivial to bruteforce a router key which would have an *router_id* the right range to be selected as 
one of the HidServ directories for the selected hidden service.

For the next 24 hours until a new desc_id is created, this HidServ directory should received approximatly 1/8 of all
client requests for this service, providing a good estimate of hidden service usage.
  
### 2. Potential DoS Attacks on Tor Hidden Services (Doesn't look feasible)
The technique above could be expanded to try and generate keys and *router_id*'s the would be selected for all 6
responsible HidServ directories. These attacker controlled HidServ directories could then return no date or incorrect
responses to clients locking to connect to the attacked hidden services. As there are no other sources for this 
hidden service descriptor the hidden service would be effectivly inaccessbile, DoS'd.

I estimated only: 6 (Responsible Directories) * 2 (24 hour HidServDir Delay)) = 12 Tor instances would be required.
It is possible to have two Tor nodes per IP, therefore it should be possible to perform a full DoS of a hidden service
with just 6 static IP's.

--

Still not certain what the OR *identity_digest* identifying a OR in the DHT is. I think it is based the sha1 hash of the OR's
*server_identity* public key. This *server_identity* key is loaded from the *secret_id_key* file in Tor's key directory
and it should never change, unless we are manipulating it. The *identity digest* code in router.c 
(https://github.com/DonnchaC/tor/blob/master/src/or/router.c#L1803-L1808) 

### First results

commit #4e48bb1 works perfectly for logging requested hidden service descriptors and published descriptors. Unfortunately
worst fears of Tor hidden services were realized. First logged hidden service was a private tor marketplace, second site
was a forgotten web page from 2009, and the third site contain child abuse images. Pretty disgustings.

Definitely huge potential to scan and categorize all hidden services and check their purpose here. Would be relatively
straightforward to identify almost all child abuse sites and for LEO to begin infiltrating them. Would work for one generation
until sites start using client authentication and authentication cookies.

Shouldn't work drunk, can't remove committed spelling mistakes :)
