"""
This file contains the server class and its subclasses.
It is used to create handle-able objects for the bot.
"""

#! This file is reserved for future use.
# imports
from tinydb import TinyDB, Query
import time

class server():
    """
    This class is used to create an object to handle discord guilds.
    Attributes:
    - guild_id: The id of the guild.
    
    - Flags: integer representing the flags of the server.
        - 1 << 0: server is permanently banned
        - 1 << 2: server has unlocked global premium features
        - 1 << 3: server has permanent premium & upscales [courtesy of the admins]
        - 1 << 4: server has been previously banned
        - 1 << 5: is admin server
        - 1 << 6-16: reserved for future use
    """
    def __init__(self) -> None:
        pass