"""
This file contains the user class and its subclasses.
It is used to create handle-able objects for the bot.
"""

# constants
__database__ = 'db.json'

# imports
from tinydb import TinyDB, Query
import time
from models import image


class user():
    """
    This class is used to create handle-able objects for the bot.

    Attributes:
    - uid: The user id of the user who uploaded the image.

    - joined: The time the user joined the bot.
    - last_seen: The time the user was last seen.

    - total_images: The total amount of images the user has upscaled.
    - free_images: The amount of images the user has left to upscale.
    - premium_images: the amount of premium images the user has left to upscale.
    - premium_codes: a list of premium codes a user used

    - user_flags: integer representing the flags of the user.
        - 1 << 0: user is permanently banned
        - 1 << 1: user is temporarily banned
        - 1 << 2: user has unlocked premium features
        - 1 << 3: user has permanent premium & upscales [courtesy of the admins]
        - 1 << 4: user has been previously banned
        - 1 << 5: is admin user
        - 1 << 6: has beta permissions
        - 1 << 7-16: reserved for future use 

    - images: list of all image ids the user has uploaded.
    - banned_until: the time the user is banned until. None if not banned.
    - banned_reason: the reason the user is banned. None if not banned.

    Methods:
    - __init__: initialiser for the user class.
    - __str__: returns a string representation of the user.

    - __load_from_uid: loads the user from the database using the uid.
    - __load_from_image_id: loads the user from the database using the image_id.

    - __save: saves the user to the database.
    - __pack: packs the user into a dict (for database storage).

    - fetch_flags: fetches the flags of the user.
    - __add_flag: adds a flag to the user.
    - __remove_flag: removes a flag from the user.

    - ban_user: bans the user for a certain amount of time.

    - end_user: ends the user and saves to db.
    """

    def __init__(self, **kwargs):
        """
        This function is used to initialise the user class.
        Allowed keywords:
        - uid: The user id of the user who uploaded the image.
        - image_id: The image id of an image. (will load the user who uploaded the image)
        """
        
        # initialise the user
        self.uid = kwargs.get('uid', None)
        self.image_id = kwargs.get('image_id', None)

        if self.image_id is not None and self.uid is None: # in case both are defined, set image_id to None (uid > image_id)
            self.image_id = None

        #if neither are defined, raise an error
        if self.uid is None and self.image_id is None:
            raise ValueError("No uid or image_id specified")

        self.total_images = 0
        self.joined = 0
        self.last_seen = 0
        self.free_images = 0
        self.premium_images = 0
        self.premium_codes = []
        self.user_flags = 0
        self.images = []
        self.banned_until = None
        self.banned_reason = None

        # load the user
        if self.uid is not None:
            self.__load_from_uid()
        elif self.image_id is not None:
            self.__load_from_image_id()
        else:
            raise ValueError("No uid or image_id given")


    def __str__(self):
        """
        This function is used to return a string representation of the user.
        """
        return "User: {0}".format(self.uid)


    def __load_from_uid(self):
        # get the database
        db = TinyDB(__database__)
        # get the table
        table = db.table('users')
        # get the query
        query = Query()
        # get the user
        packed = table.get(query.uid == self.uid)
        if packed is None:
            self.free_images = 5
            self.__save()
            packed = table.get(query.uid == self.uid)
        self.uid = packed['uid']
        self.total_images = packed['total_images']
        self.joined = packed['joined']
        self.last_seen = packed['last_seen']    
        self.free_images = packed['free_images']
        self.premium_images = packed['premium_images']
        self.premium_codes = packed['premium_codes']
        self.user_flags = packed['user_flags']
        self.images = packed['images']
        self.banned_until = packed['banned_until']
        self.banned_reason = packed['banned_reason']


    def __load_from_image_id(self):
        """
        this is a helper function for the user class, it fetches the uid from the image and loads from uid
        """
        # initialise an image class that loads the image
        image_obj = image.image(image_id=self.image_id)
        self.uid = image_obj.uid
        self.__load_from_uid()


    def __save(self):
        # get the db
        db = TinyDB(__database__)
        # get the table
        table = db.table('users')
        # get the query
        query = Query()
        packed = self.__pack()
        # save the user
        table.upsert(packed, query.uid == self.uid)


    def __pack(self):
        """
        Packs the user into a dict (for database storage).
        """
        packed = {
            'uid': self.uid,
            'total_images': self.total_images,
            'joined': self.joined,
            'last_seen': self.last_seen,
            'free_images': self.free_images,
            'premium_images': self.premium_images,
            'premium_codes': self.premium_codes,
            'user_flags': self.user_flags,
            'images': self.images,
            'banned_until': self.banned_until,
            'banned_reason': self.banned_reason
        }
        return packed


    def fetch_flags(self) -> list[int]:
        """
        Fetches a list of all flags the user has.
        """
        return [i for i in range(16) if self.user_flags & (1 << i)] # range is 16 because there are max 16 flags


    def __add_flag(self, flag: int) -> None:
        """
        adds a flag to the user.
        """
        self.user_flags |= 1 << flag


    def __remove_flag(self, flag) -> None:
        """
        Removes a flag from the user.
        """
        self.user_flags &= ~(1 << flag)

    #TODO add ban_user function
    def ban_user(self, time: int, reason: str) -> None:
        ...
        return NotImplemented


    def end_user(self):
        self.__save()
        del self # renders the object useless after saving
