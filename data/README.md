## Collected Hidden Service Data
===

The files in this directory contain the raw and processed data my 4 nodes collected in 2 months.

* raw_data_mongodb_export.tar.bz2 - This contains the raw request data with timestamps in 3 mongodb collections.
* observed_descriptor_ids.txt - Counts the number of requests for all descriptors received.
* desc_requests_with_serviceids.txt - Contains counts of the descriptor requests for onion address I could cross reference.
* requested_hidden_services.txt - Cotains count of client requests for hidden services. The total count might be for different descriptors for the same hidden service.
* onion_server_headers.csv - This CSV file contains the Server headers returned from some of the hidden services I scanned. It shows a common trend where many hidden services are hosted the same platform by organisations such as "Freedom Hosting". 

For getting some general information on the most popular hidden services, the *desc_requests_with_serviceids.txt* file will be most useful as it seperates the requests for each different descriptor ID. Each count represents a single 24 hour period.

The mongodb dump can be imported into a local mongo instance by extracting the archive and running the following command in the directory

   mongorestore DBNAME
