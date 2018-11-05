# Memcache-Relational-Database-Performance
Measure and improve performance of Relational database

Description:

In this Project we use world earthquake data, import into SQL and with a web interface 
allow users to find out (query) interesting information about those earthquakes, 
measure performance, and then improve performance. 

 Measure performance on SQL tables: creating, querying,  
 modifying data (tuples). 

 Get well structured data at: 
  https://earthquake.usgs.gov/earthquakes/feed/v1.0/csv.php 
  
  
  Create a SQL table, calculate time to create the table (and indexes).  
  Allow a user to specify on a web interface: 
  1. A number of random queries (up to 1000 queries of random tuples in  
     the dataset) 
  2. A restricted set of queries, similar to previous (1.) but where selection is 
     restricted (ie only occurring in CA, or within N<100 km of a specified 
     lat,long location. 
     Or: a time range, or a magnitude range. 
  3. Measure time expended to perform these queries. 
  4. Show results. 

  Users of this service will interact with your performance service through web 
  page interfaces, all processing and web service hosting is (of course) cloud  
  based. 
 
