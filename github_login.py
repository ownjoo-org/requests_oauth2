import argparse
import logging

from json import loads
from typing import Optional

from requests import Response
from requests_oauthlib import OAuth2Session

import http.client

log_level: int = logging.ERROR
http.client.HTTPConnection.debuglevel = log_level
logging.basicConfig()
logging.getLogger().setLevel(log_level)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(log_level)
requests_log.propagate = True


def main(
        client_id: str,
        client_secret: str,
        target_url: Optional[str] = None,
        proxies: Optional[dict] = None,
) -> Response:
    session = OAuth2Session(client_id=client_id)
    session.proxies = proxies
    session.headers = {'Accept': 'application/json'}

    start_url = 'https://github.com/login/oauth/authorize'
    token_url = 'https://github.com/login/oauth/access_token'

    authorization_url, state = session.authorization_url(start_url)
    print(f'Authorize here: {authorization_url}')

    redirect_response = input('Redirect URL: ')
    session.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)

    return session.get(target_url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--client_id',
        type=str,
        required=True,
        help='The user name for your IdP account',
    )
    parser.add_argument(
        '--client_secret',
        type=str,
        required=True,
        help='The password for your IdP account',
    )
    parser.add_argument(
        '--target_url',
        type=str,
        required=True,
        help='Target URL after login',
    )
    parser.add_argument(
        '--proxies',
        type=str,
        required=False,
        help="JSON structure specifying 'http' and 'https' proxy URLs",
    )

    args = parser.parse_args()

    proxies: Optional[dict] = None
    if args.proxies:
        proxies: dict = loads(args.proxies)

    if data := main(
        client_id=args.client_id,
        client_secret=args.client_secret,
        target_url=args.target_url,
        proxies=proxies,
    ):
        print(data)
    else:
        print('whoops...')
