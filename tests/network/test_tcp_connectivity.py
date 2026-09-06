import socket
from urllib.parse import urlparse


def test_api_tcp_connectivity(base_url):

    parsed_url = urlparse(base_url)

    host = parsed_url.hostname
    port = parsed_url.port or 80

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.settimeout(5)

    try:

        result = sock.connect_ex(
            (host, port)
        )

        assert result == 0

    finally:

        sock.close()


def test_unreachable_port():

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.settimeout(1)

    try:

        result = sock.connect_ex(
            ("127.0.0.1", 65530)
        )

        assert result != 0

    finally:

        sock.close()