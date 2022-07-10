"""
This file works with the stats command.
the classes present here are used to create the stats command.
"""
from tinydb import TinyDB, Query


class stats():
    """
    This is the class for the stats command that connects to the database.
    """

    def __init__(self) -> None:
        self.db = TinyDB('db.json')

    def get_user_stats(self, user_id: int) -> dict:
        """
        This function gets the stats of a user.
        :param user_id: The id of the user.
        :return: A dictionary with the stats of the user.
        """
        table = self.db.table('users')
        user_query = Query()
        user_stats = table.get(user_query.user_id == user_id)
        return user_stats[0]

    def get_server_stats(self, server_id: int) -> dict:
        """
        This function gets the stats of a server.
        :param server_id: The id of the server.
        :return: A dictionary with the stats of the server.
        """
        return NotImplemented # TODO: implement this
        table = self.db.table('servers')
        server_query = Query()
        server_stats = table.get(server_query.server_id == server_id)
        return server_stats[0]

    def get_global_stats(self) -> dict:
        """
        This function gets the stats of the bot.
        :return: A dictionary with the stats of the bot.
        """
        return NotImplemented