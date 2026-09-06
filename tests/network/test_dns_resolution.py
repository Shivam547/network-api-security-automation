import socket


def test_localhost_dns_resolution():

    ip_address = socket.gethostbyname(
        "localhost"
    )

    assert ip_address in {
        "127.0.0.1",
        "::1"
    }