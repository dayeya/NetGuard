"""
Author: Daniel Sapojnikov 2023.
Client Class used to define clients across the LAN.
"""

from socket import socket
from typing import Tuple, Union
from dataclasses import dataclass

type Address = Tuple[str, int]

@dataclass(slots=True)
class Connection:
    sock: socket
    host_addr: Address

    @property
    def address(self) -> Address:
        return self.host_addr
    
    def close(self) -> None:
        self.sock.close()
        
    def __hash__(self) -> int:
        return hash((self.sock, self.host_addr))

class ClientConnection(Connection):
    def __init__(self, sock: socket, addr: Address) -> None:
        super().__init__(sock, addr)
        
    def __repr__(self) -> str:
        return f'ClientConnection(sock={self.sock}, addr={self.host_addr})'

class ServerConnection(Connection):
    def __init__(self, sock: socket, addr: Address) -> None:
        super().__init__(sock, addr)
        
    def __repr__(self) -> str:
        return f'ServerConnection(sock={self.sock}, addr={self.host_addr})'

type ConnectionType = Union[ClientConnection, ServerConnection]
type NetworkObject = Union[ConnectionType, socket]

def close_all(*objects: Tuple[NetworkObject]) -> None:
    """
    Closes all network objects that have .close()
    """
    for closeable in objects:
        classify = closeable.__class__.__name__
        try:
            closeable.close()
            print(f'[!] A {classify} object was closed successfuly!')
        except Exception as close_error:
            print(f'[!] {classify}.close() was not complete. {close_error}')
            
def conn_to_str(conn_type: ConnectionType) -> str:
    """
    Converts the ConnectionType into a string.
    :params: conn_type.
    :returns: repr string.
    """
    return repr(conn_type)[:6].lower()