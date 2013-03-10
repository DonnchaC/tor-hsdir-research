#!/usr/bin/env python
from time import time
from base64 import b32encode, b32decode, b16decode
from hashlib import sha1
from struct import pack, unpack
import argparse
import datetime, calendar

# When provided with a Tor hidden service 'service_id', this script should output
# the predicted desc_id's which will be used to publish the HS descriptors for this
# HS into the future.

# Based on rend_compute_v2_desc_id() from rendcommon.c in Tor source code.
def compute_desc_ids(service_id_base32, max_replicas, time = int(time()), descriptor_cookie = ""):
  desc_ids = []
  for replica in range(0, max_replicas):
    desc_ids.append(rend_compute_v2_desc_id(service_id_base32, replica, time, descriptor_cookie))
  return desc_ids

# Returns base_32 encode desc_id - descriptor-id = H(permanent-id | H(time-period | descriptor-cookie | replica))
def rend_compute_v2_desc_id(service_id_base32, replica, time, descriptor_cookie):#
   service_id = b32decode(service_id_base32, 1)
   time_period = get_time_period(time, 0, service_id)
   secret_id_part = get_secret_id_part_bytes(time_period, descriptor_cookie, replica)
   desc_id = rend_get_descriptor_id_bytes(service_id, secret_id_part)
   return b32encode(desc_id).lower()

# Calculates time period - time-period = (current-time + permanent-id-byte * 86400 / 256) / 86400
def get_time_period(time, deviation, service_id):
  REND_TIME_PERIOD_V2_DESC_VALIDITY = 24 * 60 * 60
  return int(((time + ((unpack('B', service_id[0])[0] * REND_TIME_PERIOD_V2_DESC_VALIDITY) ) / 256) ) / REND_TIME_PERIOD_V2_DESC_VALIDITY + deviation)

# Calculate secret_id_part - secret-id-part = H(time-period | descriptor-cookie | replica)
def get_secret_id_part_bytes(time_period, descriptor_cookie, replica):
  secret_id_part = sha1()
  secret_id_part.update(pack('>I', time_period)[:4]);
  if descriptor_cookie:
    secret_id_part.update(descriptor_cookie)
  secret_id_part.update('{0:02X}'.format(replica).decode('hex'))
  return secret_id_part.digest()

def rend_get_descriptor_id_bytes(service_id, secret_id_part):
  descriptor_id = sha1()
  descriptor_id.update(service_id)
  descriptor_id.update(secret_id_part)
  return descriptor_id.digest()

# Return the time of day when the desc_id changes for this service
def time_desc_changes(service_id, time = int(time())):
  orig_time_period = get_time_period(time, 0, service_id)
  while (get_time_period(time, 0, service_id) == orig_time_period):
    time += 1
  # time_period has now changed. return the time of day.
  return time

def main():
    REPLICAS = 2
    
    parser = argparse.ArgumentParser(description="This tool allows you to generate the desc_id's that will " \
                                                 "be used by hidden services at any past or future date. " \
                                                 "By default the current desc_id id's for the hidden service " \
                                                 "are returned)")
    parser.add_argument('onion_address', help='The hidden service address - e.g. (idnxcnkne4qt76tg.onion)')
    parser.add_argument("-d", "--days", type=int,
                    help="Number of days into the future to generate desc_id's")
    parser.add_argument("-p", "--past", action="store_true",
                    help="Should we generate desc_id's for dates in the past instead of the future")
    args = parser.parse_args()

    service_id, tld = args.onion_address.split(".")
    if tld == 'onion' and len(service_id) == 16 and service_id.isalnum():   
        time_desc_updates = datetime.datetime.fromtimestamp(time_desc_changes(service_id)) - datetime.timedelta(days = 1)
                  
        if args.days: # Calculate desc_id's for future dates
          for day in range(0, args.days):
            desc_ids = compute_desc_ids(service_id, REPLICAS, calendar.timegm(time_desc_updates.timetuple()))
            print time_desc_updates.strftime('%Y-%m-%d %H:%M:%S') + '\t' + '\t'.join(desc_ids)
            if args.past:
              time_desc_updates = time_desc_updates - datetime.timedelta(days = 1)
            else:
              time_desc_updates = time_desc_updates + datetime.timedelta(days = 1)
    
        else: # Output the current desc_id's for the specified hidden service
          desc_ids = compute_desc_ids(service_id, REPLICAS, calendar.timegm(time_desc_updates.timetuple()))
          print time_desc_updates.strftime('%Y-%m-%d %H:%M:%S') + '\t' + '\t'.join(desc_ids)
    else:
      print "[!] The onion address you provided is not valid"
  
if __name__ == '__main__':
    main()
