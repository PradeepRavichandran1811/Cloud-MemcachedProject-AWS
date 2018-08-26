
# Python Flask app on Amazon Web Services-Elastic Beanstalk

This web application is developed by using Python and Flask. It performs randomly generated queries on a earthquake dataset using some constraints given by the user. 

Amazon's Memcache(ElastiCache) was used in this project to optimize the execution time of randomly generating queries. It also has an implementation without using memcache so that one can compare the execution time so that one can decide whether they really need memcache.

This project was deployed and tested on AWS Elastic Beanstalk.

JMeter was used to test the performance, load and response time when numerous number of requests comes in a second.
