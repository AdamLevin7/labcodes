#TODO finish the last 3 modules in this script
"""
Script: server_connection
    Connect to a mySQL database on a server through SSH tunnel.

Modules
    open_ssh_tunnel: Open an SSH tunnel and connect using a username and password.
    mysql_connect: Connect to a MySQL server using the SSH tunnel connection
    mysql_disconnect: Disconnect from MySQL
    close_ssh_tunnel: Close SSH Tunnel

Author:
    Casey Wiens
    cwiens32@gmail.com
"""


def open_ssh_tunnel(ssh_host, ssh_username, ssh_password, verbose=False):
    """
    Function::: open_ssh_tunnel
    	Description: Open an SSH tunnel and connect using a username and password.
    	Details:

    Inputs
        ssh_host: SSH tunnel host name
        ssh_username: SSH tunnel user name
        ssh_password: SSH tunnel password
        verbose: Set to True to show logging

    Outputs
        tunnel: SSH tunnel connection

    Dependencies
        sshtunnel
        logging
    """

    # Dependencies
    import sshtunnel
    import logging

    if verbose:
        sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG

    tunnel = sshtunnel.SSHTunnelForwarder(
        (ssh_host, 22),
        ssh_username=ssh_username,
        ssh_password=ssh_password,
        remote_bind_address=('127.0.0.1', 3306)
    )

    tunnel.start()

    return tunnel


def mysql_connect(database_username, database_password, database_name, tunnel):
    """Connect to a MySQL server using the SSH tunnel connection

    :param database_username: MySQL database host name
    :param database_password: MySQL database user name
    :param database_name: MySQL database password
    :param tunnel: SSH tunnel connection
    :return connection: MySQL database connection
    """

    # Dependencies
    import pymysql

    connection = pymysql.connect(
        host='127.0.0.1',
        user=database_username,
        passwd=database_password,
        db=database_name,
        port=tunnel.local_bind_port
    )

    return connection


def mysql_disconnect(connection):
    """Closes the MySQL database connection.

    :param connection: MySQL database connection
    """

    connection.close()


def close_ssh_tunnel(tunnel):
    """Closes the SSH tunnel connection.
    """

    tunnel.close


