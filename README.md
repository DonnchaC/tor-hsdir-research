# Tor Hidden Service (DHT) Research
===

This repository contains a modified version of the Tor client and related scripts for investigating attacks
on the Tor hidden service distribute hash table.

The raw data I captured is is the *data* directory and other scripts and tools are in the *scripts* directory.

Currently the following data is being logged to Tor's notice logs:
* When HS directory receives a v2 hidden service descriptor - rend_cache_store_v2_desc_as_dir() - rendcommon.c
* When HS directory receives a client request for a v2 hidden service descriptor - directory.c - Line 3245
* The requested *service_id* is stored when a client requests a desc_id we have stored in our HS descriptor list - directory.c

Please check out my [blog post](http://donncha.is/2013/05/trawling-tor-hidden-services/) for more information.

==
## Other information

The information below is a working summary of this research as I was trying to figure things out. 
Be advised there might be mistakes here, but I'll leave it up as a summary

--

### Background
Tor hidden service desc_id's are deterministic and if there is no 'descriptor cookie' anyone can determined
the desc_id's for a HS at an arbitrary point in time. In fact this is required as this is the mechanism by
which OP's request hidden service descriptors from the HS directories. They are calulated as follows:

    descriptor-id = H(permanent-id | H(time-period | descriptor-cookie | replica))

*decriptor-cookie* is typically empty. *replica* is an integer, usual from 0-1 which indicated the set of 
HidServ directories responsible for this descriptor and *permanent-id* is derived from the service public key.

    time-period = (current-time + permanent-id-byte * 86400 / 256) / 86400

The *time-period* changes approximatly every 24 hours. The first byte of the *permanent_id* is added to ensure
that hidden services do not all try to update at the same time.

    identity-digest = H(server-identity-key)
    
The identity-digest is the SHA1 hash of the public key from the *secret_id_key* file in Tor's DATA/keys directory.
Normally it should never change for an OR as it is used in the calculation of its router fingerprint, but the key is
completely user controlled. The *identity digest* code is in router.c - 
(https://github.com/DonnchaC/tor/blob/master/src/or/router.c#L1803-L1808) 

The HidServ directory with *identity-digest* will be picked as responsible if it is one of the three HS
directories before the *descriptor-id* in a descending lists of all HidServ directories. By default the HS descriptor
will be published to two *replica*'s (set's of 3 HS directories at different points of the router list). The HS
*descriptor-id*'s for each *replica* will be different.

### 1. Statistical and Traffic Analysis of Tor Hidden Services
It is possible to determine more than 24 hours in advanced what a public hidden service's *desc_id* will be, based on
the background and spec's above. It is then trivial to bruteforce a router key which has an *identity_digest* in
the right range to be selected as one of it's HS directories. Example code for this is provided in
scripts/identity_key_generator/ which is based on the 'shallot' software for generating vanity .onion addresses.

For the next 24 hours until a new desc_id is created, this HidServ directory should received approximatly 1/6 of all
client requests for this service, providing a good estimate of hidden service usage. This data can be made more
accurate by creating more Tor HS directories which will have *identity_digest*'s in the responsible range up to a
point where all of the responsible HS directories are controlled by you.
  
### 2. Potential DoS Attack on Tor Hidden Services
The method outline above could be expanded to generate keys and *router_id*'s the would be selected as all 6
responsible HidServ directories for a targeted HS. These attacker controlled HS directories could then return
no data (404 Response) to an OP looking to download the HS's descriptor and in turn connect to the HS. As there
are no other sources for this HS descriptor it would be impossible for a OP to access the HS and a result
the hidden service would be effectivly DoS'd.

I estimated only: 6 (Responsible Directories) * 2 (24 hour HidServDir Delay)) = 12 Tor instances would be required to
affect an indefinite DoS attack on a HS. It is possible to have two Tor HS directories per IP, therefore it should be
possible to perform a full DoS attack with just 6 static IP's.
