from queue import Queue
from threading import Thread
from datetime import datetime
import json
from collections import deque
from dataclasses import dataclass

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt, IntPrompt

from game import connect_to_queue, login, request_match, request_scoreboard
from weapons import Weapons


ip = Prompt.ask("Enter server IP", default="localhost")
port = IntPrompt.ask("Enter RCON port", default=42070)
password = Prompt.ask("Enter RCON password", default="admin")

console = Console()

q = Queue()
sock = login(ip, port, password)

@dataclass
class PlayerLookup:
    player_lookup = {}

    def update_player_lookup(self, packet):
        for key in packet:
            if "PlayerData" in key:
                player_packet = packet[key]
                self.player_lookup[player_packet['ID']] = player_packet

    def get_name(self, player_id):
        if player_id in self.player_lookup:
            return self.player_lookup[player_id]['Name']
        return "Unknown"

lookup_table = PlayerLookup()

# Need to sleep to send a subsequent rocn command
import time; time.sleep(0.2)
request_match(sock)
time.sleep(0.2)
request_scoreboard(sock)

bmrcon_thread = Thread(target=connect_to_queue, args=(sock, q), daemon=True)
bmrcon_thread.start()

def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="status", size=3),
        Layout(name="top" ),
        Layout(name="body", ratio=1),
    )
    layout['top'].split_row(
        Layout(name="scoreboard", ratio = 3),
        Layout(name="loadouts", ratio = 1)
    )
    layout['body'].split_row(
        Layout(name="chatbox", ratio = 3),
        Layout(name="killfeed", ratio = 1)
    )
    return layout




layout = make_layout()
layout['body'].update(Text('Messages will show up here'))

from rich.live import Live
from time import sleep

def format_message(message_packet: dict):
    return f"{message_packet['Name']}: {message_packet['Message']}"

def make_chatbox(packets: list):
    chat_message = Table.grid(padding=1)
    chat_message.add_column(style="green", justify="right")
    chat_message.add_column(no_wrap=True)
    for packet in packets:
        chat_message.add_row(
            packet['Name'],
            packet['Message']
        )
    
    message_panel = Panel(
        chat_message,
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b red]Chat messages!",
        border_style="bright_blue",
    )
    return message_panel



def make_loadouts(packets):
    loadout_feed = Table.grid(padding=1)
    loadout_feed.add_column(style="green", justify="right")
    loadout_feed.add_column()
    loadout_feed.add_column()

    for packet in packets:
        loadout_feed.add_row(
            lookup_table.get_name(packet['PlayerID']),
            Weapons(int(packet['Weap1'])).name,
            Weapons(int(packet['Weap2'])).name,
        )
    
    loadout_panel = Panel(
        loadout_feed,
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b red]Loadoutfeed!",
        border_style="bright_blue",
    )
    return loadout_panel


def make_killfeed(packets: list):
    killfeed = Table.grid(padding=1)
    killfeed.add_column(style="green", justify="right")
    killfeed.add_column(no_wrap=True)
    killfeed.add_column(style="red", justify="right")

    for packet in packets:
        killfeed.add_row(
            lookup_table.get_name(packet['KillerID']),
            Weapons(int(packet['KillerWeapon'])).name,
            lookup_table.get_name(packet['VictimID']),
        )
    
    killfeed_panel = Panel(
        killfeed,
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b red]Killfeed!",
        border_style="bright_blue",
    )
    return killfeed_panel


def fixed_append(deq: deque, packet: dict, event_id: str):
    if packet['EventID'] == event_id:
        if len(deq) > 10:
            deq.popleft()
        deq.append(packet)


def make_status(packet):
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_column()
    grid.add_column()
    grid.add_column()
    grid.add_column(justify="right")
    grid.add_row(
        "Boring Man TUI", 
        f"[bold magenta]{packet['ServerName']}", 
        f"[bold magenta]{packet['Map']}", 
        f"[bold magenta]{packet['Players']}/{packet['MaxPlayers']}",
        datetime.now().ctime().replace(":", "[blink]:[/]"),
    )
    return Panel(grid)



def make_scoreboard(packet, team, two_team=True):
    
    if two_team:
        score = f'Team{team}Score'
        table = Table(title=f"Team {team} Score: {packet[score]}", expand=True)
    else:
        table = Table(title="Scoreboard", expand=True)

    
    table.add_column("Name", justify="", style="cyan", no_wrap=True)
    table.add_column("Kills", style="magenta")
    table.add_column("Assists", style="blue")
    table.add_column("Deaths", justify="right", style="red")
    for key in packet:
        if "PlayerData" in key:
            player_packet = packet[key]
            if player_packet['Team'] == team:
                table.add_row(
                    player_packet['Name'],
                    player_packet['Kills'],
                    player_packet['Assists'],
                    player_packet['Deaths']
                )
    return table


def make_scoreboard_panel(packet):
    grid = Table.grid(expand=True)
    grid.add_column(justify='right')
    grid.add_column(justify='right')
    table = make_scoreboard(packet, "1")
    table2 = make_scoreboard(packet, "2")
    
    grid.add_row(
        table,
        table2
    )
    return Panel(grid)


with Live(layout, refresh_per_second=10, screen=True):
    chat_queue = deque()
    kill_queue = deque()
    loadout_queue = deque()
    while True:
        packet = q.get()
        fixed_append(chat_queue, packet, "42")
        fixed_append(kill_queue, packet, "6")
        fixed_append(loadout_queue, packet, "62")
        layout['chatbox'].update(make_chatbox(list(chat_queue)))
        layout['killfeed'].update(make_killfeed(list(kill_queue)))
        layout['loadouts'].update(make_loadouts(list(loadout_queue)))
        if packet['EventID'] == '34': 
            if packet['CaseID'] == "7":
                layout['scoreboard'].update(make_scoreboard_panel(packet))
                lookup_table.update_player_lookup(packet)
            if packet['CaseID'] == "5":
                layout['status'].update(make_status(packet))
                