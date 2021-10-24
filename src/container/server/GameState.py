from subprocess import Popen, PIPE
from typing import Dict, List
import os
import signal
from threading import Thread
import time
from enum import Enum

import psutil

from SettingsModel import FullSettings
from healthcheck import health_check

SUBPROCESS_DIFFERENCE = 39

class ServerMode(Enum):
    normal = 1
    healthcheck = 2
    permanent = 3


class GameState:
    """A class for managing the state for a single server"""
    def __init__(self, game_port: int, rcon_port: int, display: int):
        self.game_port = game_port
        self.rcon_port = rcon_port
        self.display = display
        self.settings = None
        self.is_allocated = False
        self.game_id = None
        self.pid = None


    def allocate(self, game_id: int, settings: FullSettings, mode: ServerMode):
        """Allocate a new server"""
        process = Popen([
                'xvfb-run',
                '--server-num=%d' % self.display,
                '/bm/BoringManRewrite',
                '-dedicated_nogpu',
                '-vanillaGFX',
                '-server',
                f'custom{game_id}'
            ],
            stdout = PIPE, 
            stderr = PIPE, 
        )
        # Sleep 1 second to wait for the process to initialize
        time.sleep(1)
        self.is_allocated = True
        self.game_id = game_id
        self.settings = settings
        self.pid = get_server_pid(game_id)
        if mode == ServerMode.healthcheck:
            t = Thread(target=run_healthchecks_periodically, args=(self,), daemon=True)
            t.start()
        if mode == ServerMode.permanent:
            t = Thread(target=restart_stopped_server, args=(self,), daemon=True)
            t.start()
        if mode == ServerMode.normal:
            pass


    def deallocate(self):
        """Deallocate a server"""
        self.is_allocated = False
        self.game_id = None
        self.settings = None
        self.pid = None
        

    def get_game_info(self) -> Dict:
        """Returns a dictionary of information about the server"""
        return {
            'game_port': self.game_port,
            'rcon_port': self.rcon_port,
            'game_id': self.game_id,
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
                    mapping['rcon_port'],
                    mapping['display']
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
                if not psutil.pid_exists(server.pid):
                    server.deallocate()



def run_healthchecks_periodically(
    gamestate: GameState,
    retries=10,
    delay=12,
    initial_delay=30
):
    """Run the healthcheck function 
    until it fails {retries} number of times in a row.
    delay determines the length of time between healthchecks
    initial_delay time is waited before beginning health checks
    """
    time.sleep(initial_delay)
    failure_counter = 0
    while failure_counter != retries:
        if not health_check(gamestate.settings):
            failure_counter += 1
        else:
            failure_counter = 0
        time.sleep(delay)
    os.kill(gamestate.pid)
    gamestate.deallocate()
    

def restart_stopped_server(gamestate: GameState, frequency = 15):
    """Rerun the server if it stopped"""
    while gamestate.is_allocated:
        if not psutil.pid_exists(gamestate.pid):
            gamestate.allocate(gamestate.game_id, gamestate.settings, ServerMode.normal)
        time.sleep(frequency)


def get_server_pid(game_id: int):
    """Returns the PID of the server. If not found, return -1"""
    for proc in psutil.process_iter():
        if (
            len(proc.cmdline()) > 0
            and proc.cmdline()[0] == '/bm/BoringManRewrite'
            and f'custom{game_id}' in proc.cmdline()
        ):
            return proc.pid
    return -1