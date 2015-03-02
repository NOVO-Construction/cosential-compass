import argparse
import sys
from getpass import getpass

from compass import CompassClient, CompassClientException


def main():
    parser = argparse.ArgumentParser(description="Usage: %prog [options] ")
    parser.add_argument('--username', dest='username', help='Cosential username')
    parser.add_argument('--password', dest='password', help='Cosential password')
    parser.add_argument('--firm-id', dest='firm_id', help='Cosential firm id')
    parser.add_argument('--api-key', dest='api_key', help='Cosential api key')
    parser.add_argument('--debug', dest='debug', help='Debug', action='store_true')
    parser.add_argument('--test', dest='test', help='Use test url', action='store_true')
    args = parser.parse_args()
    username = args.username
    password = args.password
    firm_id = args.firm_id
    api_key = args.api_key
    if not firm_id:
        firm_id = raw_input('Enter Cosential firm id: ')
    if not api_key:
        api_key = raw_input('Enter Cosential api key: ')
    if not username:
        username = raw_input('Enter Cosential username: ')
    if not password:
        password = getpass(prompt='Enter password for {0}: '.format(username))
    print('Fetching user token from Cosential...')
    if args.test:
        client = CompassClient(endpoint='compass.uat')
    else:
        client = CompassClient()
    try:
        user_token = client.get_user_token(username=username, password=password, firm_id=firm_id, api_key=api_key)
    except CompassClientException as e:
        print(e)
        sys.exit()
    if user_token is None:
        print('Could not retrieve compass user token.  Make sure your firm id, api key, username and password are correct.')
        main()
    print("{0}'s user token is: {1}".format(username, user_token))
    sys.exit()


if __name__ == '__main__':
    main()
