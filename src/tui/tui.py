from queue import Queue
from threading import Thread
from datetime import datetime
import json
from collections import deque

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt, IntPrompt

from game import connect_to_queue, login


ip = Prompt.ask("Enter server IP", default="")
port = IntPrompt.ask("Enter RCON port", default=0)
password = Prompt.ask("Enter RCON password", default="")

console = Console()

q = Queue()
sock = login(ip, port, password)

bmrcon_thread = Thread(target=connect_to_queue, args=(sock, q), daemon=True)
bmrcon_thread.start()

def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="scoreboard" ),
        Layout(name="body", ratio=2),
    )
    layout['body'].split_row(
        Layout(name="chatbox"),
        Layout(name="killfeed")
    )
    return layout


class Header:
    """Display header with clock."""
    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "Boring Man TUI",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid)



layout = make_layout()
layout["header"].update(Header())
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


def make_killfeed(packets: list):
    killfeed = Table.grid(padding=1)
    killfeed.add_column(style="green", justify="right")
    killfeed.add_column(no_wrap=True)
    killfeed.add_column(style="red", justify="right")

    for packet in packets:
        killfeed.add_row(
            packet['VictimID'],
            packet['KillerWeapon'],
            packet['KillerID']
        )
    
    killfeed_panel = Panel(
        killfeed,
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b red]Killfeed!",
        border_style="bright_blue",
    )
    return killfeed_panel

def fixed_append(deq: deque, packet: dict, event_id: string):
    if packet['EventID'] == event_id:
        if len(deq) > 10:
            deq.popleft()
        deq.append(packet)


with Live(layout, refresh_per_second=10, screen=True):
    chat_queue = deque()
    kill_queue = deque()
    while True:
        packet = q.get()
        fixed_append(chat_queue, packet, "42")
        fixed_append(chat_queue, packet, "6")
        layout['chatbox'].update(make_chatbox(list(chat_queue)))
        layout['killfeed'].update(make_killfeed(list(kill_queue)))

        