import os
import socket
from pathlib import Path

from hyprgest.config import COMMANDS
from hyprgest.models import Gesture


def _get_socket_path() -> Path:
    runtime_dir = os.environ["XDG_RUNTIME_DIR"]
    signature = os.environ["HYPRLAND_INSTANCE_SIGNATURE"]
    return Path(runtime_dir) / "hypr" / signature / ".socket.sock"


def send_command(command: str) -> str:
    sock_path = _get_socket_path()
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.connect(str(sock_path))
        sock.sendall(f"{command}\n".encode())
        return sock.recv(1024).decode("utf-8")


def execute_gesture(gesture: Gesture) -> None:
    if command := COMMANDS.get(gesture):
        send_command(command)
