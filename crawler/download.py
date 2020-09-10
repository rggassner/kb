#!/usr/bin/python3
import socks
import socket
import json
import sys

#def create_connection(address, timeout=None, source_address=None):
#    sock = socks.socksocket()
#    sock.connect(address)
#    return sock
#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
#socket.socket = socks.socksocket
#socket.create_connection = create_connection
import urllib.request
from urllib.error import HTTPError
from urllib.error import ContentTooShortError

i = 1
while i <= 3:
    try:
        urllib.request.urlretrieve(sys.argv[1],sys.argv[2])
        break
    except HTTPError as err:
        print("Error: %s, reason: %s. Retrying (%i).." % (err.code, err.reason, i))
        i = i+1
    except IOError as err:
        print("Error: %s, reason: %s. Retrying (%i).." % (err.errno, err.strerror, i))
        i = i+1
    except socket.timeout as err:
        print("Network error: %s. Retrying (%i).." % (err.strerror, i))
        i = i+1
    except socket.error as err:
        print("Network error: %s. Retrying (%i).." % (err.strerror, i))
        i = i+1
    except ContentTooShortError as err:
        print("Error: The downloaded data is less than the expected amount, so skipping.")
        i = i+1
if i >= 3:
    sys.exit(1)
sys.exit(0)
