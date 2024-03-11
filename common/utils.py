def build_connection_url(
        protocol: str,
        user: str,
        password: str,
        host: str,
        port: str,
        virtual_host: str
):
    host = f"{host}:{port}" if port else host
    connection_url = f"{protocol}://{user}:{password}@{host}/{virtual_host}"
    return connection_url


def build_default_connection_url():
    return build_connection_url('ampq', 'guest', 'guest', 'localhost', '5672', '/')
