from subprocess import Popen, PIPE
from typing import Dict, List
import os
import signal
from threading import Thread
import time

from healthcheck import health_check

def check_pid(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


class GameState:
    """A class for managing the state for a single server"""
    def __init__(self, game_port: int, rcon_port: int):
        self.game_port = game_port
        self.rcon_port = rcon_port
        self.is_allocated = False
        self.game_id = None
        self.pid = None


    def allocate(self, game_id: int, healthcheck = True):
        """Allocate a new server"""
        process = Popen(f'/root/BoringManRewrite -server custom{game_id}', stdout=PIPE, stderr=PIPE, shell=True)
        self.pid = process.pid
        self.is_allocated = True
        self.game_id = game_id
        if healthcheck:
            t = Thread(target=run_healthchecks_periodically, args=(self,), daemon=True)
            t.start()


    def deallocate(self):
        """Deallocate a server"""
        os.kill(self.pid, signal.SIGTERM)
        self.is_allocated = False
        self.pid = None
        self.game_id = None
    

    def get_game_info(self) -> Dict:
        """Returns a dictionary of information about the server"""
        return {
            'game_id': self.game_id,
            'game_port': self.game_port,
            'rcon_port': self.rcon_port,
            'pid': self.pid if self.is_allocated else None 
        }
    

class ServerGameState:
    """A class for managing the state of all the servers and allocating and deallocating servers"""
    
    def __init__(self, port_mappings: List[Dict]):
        self.servers = []
        for mapping in port_mappings:
            self.servers.append(
                GameState(
                    mapping['game_port'],
                    mapping['rcon_port']
                )
            )
    

    def find_free_server(self) -> GameState:
        """Finds a server that hasn't been allocated yet"""
        for server in self.servers:
            if not server.is_allocated:
                return server
        return None


    def get_server(self, game_id: int) -> GameState:
        """Returns the server with the given game id"""
        for server in self.servers:
            if server.game_id == game_id:
                return server
        return None


    def stop_server(self, game_id: int):
        """Removes the server with the given game id"""
        server = self.get_server(game_id)
        if server is None:
            raise Exception("No server with that id")
        server.deallocate()


    def get_server_list(self) -> List[Dict]:
        """Returns a list of all the servers"""
        server_list = []
        for server in self.servers:
            server_list.append(server.get_game_info())
        return server_list


    def refresh(self):
        """Deallocates servers that are no longer running
        otherwise do nothing
        """
        for server in self.servers:
            if server.is_allocated:
                if not check_pid(server.pid):
                    server.deallocate()



def run_healthchecks_periodically(
    gamestate: GameState,
    retries=3,
    delay=60,
    initial_delay=120
):
    """Run the healthcheck function 
    until it fails {retries} number of times in a row.
    delay determines the length of time between healthchecks
    initial_delay time is waited before beginning health checks
    """
    time.sleep(initial_delay)
    failure_counter = 0
    while failure_counter != retries:
        if not health_check(gamestate.game_id):
            failure_counter += 1
        else:
            failure_counter = 0
        time.sleep(delay)
    gamestate.deallocate()
    