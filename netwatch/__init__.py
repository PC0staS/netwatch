"""
NetWatch - Network Monitor
A beautiful console-based network monitoring tool with ASCII graphs
"""

__version__ = "1.0.0"
__author__ = "PC0staS"
__email__ = "pablocostasnieto@gmail.com"
__description__ = "A beautiful console-based network monitoring tool with ASCII graphs"

from .monitor import NetworkMonitor, Colors, bytesToHuman
from .cli import main

__all__ = ["NetworkMonitor", "Colors", "bytesToHuman", "main"]
