"""
This file handles all the user settings
Currently supported settings:
- lookup free upscales left
- lookup premium upscales left
- change to ephemeral upscale
"""

# imports
from models import user
from other_files import embeds

class settings():
    """
    This class handles all the user settings
    Attributes:
    - user: the user object of the user

    Methods:
    - show: shows the main settings page
    """
    def __init__(self,uid: int) -> None:
        self.user = user.user(uid=uid) # initialize user object


    def show(self):
        ...