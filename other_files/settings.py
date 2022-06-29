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
    def __init__(self, ctx, uid: int) -> None:
        """
        Initialises the settings by user.
        Ctx is needed to fetch the user's current avatar for setting embeds
        """
        # get the user name and avatar
        self.username = ctx.author.name
        self.avatar = ctx.author.avatar_url

        # initialize user object
        self.user = user.user(uid=uid)

        # fetches the data from the database
        self.settings = self.user.settings
        self.free_upscales_left = self.user.free_images

    async def show(self):
        """
        This functions fetches and shows all the current settings the user has
        Current known settings:
        - Ephemeral: Bool
        - Free_upscales_left: int
        """
        await self.ctx.respond(embed=embeds.settingsEmbeds().show(self.avatar, self.username))
        