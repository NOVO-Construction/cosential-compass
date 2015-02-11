import argparse
import sys
from getpass import getpass

from compass import CompassClient

client = CompassClient()


def main():
    parser = argparse.ArgumentParser(description="Usage: %prog [options] ")
    parser.add_argument('--username', dest='username', help='Cosential username')
    parser.add_argument('--password', dest='password', help='Cosential password')
    parser.add_argument('--firm-id', dest='firm_id', help='Cosential firm id')
    parser.add_argument('--api-key', dest='api_key', help='Cosential api key')
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
    user_token = client.get_user_token(username=username, password=password, firm_id=firm_id, api_key=api_key)
    if user_token is None:
        print('Cound not retieve user token.  Make sure your firm id, api key, username and password are correct')
        main()
    print("{0}'s user token is: {1}".format(username, user_token))
    sys.exit()


if __name__ == '__main__':
    main()
