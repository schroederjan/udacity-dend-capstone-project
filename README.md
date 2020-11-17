# udacity-dend-capstone-project
> Capstone Project for Udacity's Data Engineering Nanodegree

## Table of contents
* [Introduction](#introduction)
* [Dependencies](#dependencies)
* [Linkes](#links)
* [Contact](#contact)

## Introduction

This is my Capstone Project for the Udacity Data Engineering Nanodegree.
To follow along with the description in the Jupyter Notebook `Capstone Project Workbook.ipynb` please make sure to meet all dependencies below as described below.

## Dependencies

The project interacts with a server running TimescaleDB there are two ways to bring it up and running, locally or in the cloud. Both set ups are quite similar but I will only focus on the cloud based implementation.
I use AWS as cloud provider. AWS's EC2 instance is the easiest (and cheapest) to get the database running.
Make sure you have installed the AWS Command Line Interface from [here](http://aws.amazon.com/cli/) and have setup an own Key-Pair (let's call it "yourkey.pem").

To just simple follow along I provide a shell [scrip](https://github.com/AionosChina/udacity-dend-capstone-project/blob/main/aws-vm-timescaledb.sh) that will create a temporary EC2, which we can then SSH into. After everything we are done with testing this project, we can then just press [ENTER] and the instance will be terminated. The script provided is a modified version of Michael Wittigs "AWS in Action", which you can find [here](https://github.com/AWSinAction/code2/blob/master/chapter04/virtualmachine.sh).

1. Creating the EC2 Instance & SSH into the Server
```bash
#use a script for temporary creating an EC2 instance
chmod +x aws-vm-timescaledb.sh && ./aws-vm-timescaledb.sh

#connect to the ec2 instance with your own key
ssh -i "yourkey.pem" yourinstanceadress.compute.amazonaws.com

```
2. TimescaleDB Server Setup
The server needs to configured to accept incoming request other than the localhost.

```bash
#CONFIGURATION FOR DATABASE CONFIG FILES!
#1)
#You have to make PostgreSQL (TimescaleDB) listening for remote incoming TCP connections. To be able to reach the server remotely
#you have to add the following line into the file /etc/postgresql/12/main/postgresql.conf
#change the line here in "Connection Settings".
listen_addresses = ‘*’

#2)
#PostgreSQL (TimescaelDB) by default refuses all connections it receives from any remote address, 
#you have to relax these rules by adding this line to /etc/postgresql/12/main/pg_hba.conf
#change a specific ip or from any ip like this:
host all all 0.0.0.0/0 md5

#3)
#then restart the db with:
sudo systemctl restart postgresql
```
3. TimescaleDB Login
After we log into the TimescaleDB the first time we can set a password and create the database used in this project. (Still from inside the EC2 Instance)
```bash
#log into
sudo -u postgres psql
#change a new password
ALTER ROLE postgres WITH PASSWORD 'YOURPASSWORD';
#create a new db and log into it
CREATE DATABASE dend;
```

4. Create the Config File for this Project
The scripts used in this project will import the data base information from a private .cfg file for security reasons. To follow along please create your own file as follows:
```bash
#execute from your local machine (not EC2)
nano dwh.cfg

### CONTENT
[TIMESCALEDB]
#provides the database information for the scripts
#does not need quotes
HOST=yourinstanceadress.compute.amazonaws.com
DB_NAME=dend
DB_USER=postgres
DB_PASSWORD=YOURPASSWORD
DB_PORT=5432
```
Now everything should be ready to follow along in my [Jupyter Notebook](https://github.com/AionosChina/udacity-dend-capstone-project/blob/main/Capstone%20Project%20Workbook.ipynb). 

## Links

- More to Udacity's Data Engineering Nanodegree you can find [here](https://www.udacity.com/course/data-engineer-nanodegree--nd027).
- More to Timescale's Time-Series Database you can find [here](https://www.timescale.com/).
- An extension to this project of mine you find in my other project `Time-Series Prediction Infrastructure` [here](https://github.com/AionosChina/Time-Series-Prediction-Infrastructure). 

## Contact
Created by [Jan Schroeder](https://www.schroederjan.com/) - feel free to contact me!

