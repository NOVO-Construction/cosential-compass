# Python client for Cosential Compass RESTful API
[![Build Status](https://travis-ci.org/NOVO-Construction/cosential-compass.svg?branch=master)](https://travis-ci.org/NOVO-Construction/cosential-compass)

## Description
A python client for the [Cosential Compass RESTful API](http://compass.uat.cosential.com/home/about).

## Installation

```bash
pip install https://github.com/NOVO-Construction/cosential-compass/archive/master.zip
```

## Command line tool
There is a command line tool to assist in obtaining a Compass user token.  It requires 4 pieces of information:

1. firm id
2. api key
3. username
4. password

These can be passed in via command line arguments.  You will be prompted for any missing information

SEE: http://compass.uat.cosential.com/documentation#authentication

```bash
get_compass_token [--firm-id=<firm id>] [--api-key=<api key>] [--username=<username>] [--password=<password>]
```

## Usage

```python
from compass import CompassClient

client = CompassClient(<compass-token>)
client.get_company_schema()
client.get_company(-1)
client.get_company_list()
client.get_company_iterator()
client.search_companies(query='Austin') # Search methods seem to be broken at this time - returns 500
```

[View source](https://github.com/NOVO-Construction/cosential-compass/blob/master/compass/client.py) for list of all methods.
