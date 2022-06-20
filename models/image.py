"""
This file contains the image class and it's subclasses.
It is used to create handle-able objects for the bot.
"""

#from constants import __database__ #imports the name of the database
__database__ = 'db.json'

# imports
from tinydb import TinyDB, Query
import time
from dotenv import find_dotenv, load_dotenv
from os import getenv
import aiohttp
import json

class image():
    """
    This class is used to create handle-able objects for the bot.
    Attributes:
    - uid: The user id of the user who uploaded the image.
    - url: The url of the image on discord (ephenumeral).
    - id: The end id of the image.
        -Note: id will always be the latest id of the chevereto image, if only v1 is used, the id of v1 will also be the images id.

    - chev1: the first image link on chevereto.
    - chev2: the second image link on chevereto.
    - chev1r: the response from chevereto for the first image.
    - chev2r: the response from chevereto for the second image.
    - _rayid: the bigjpg ray id of the image.

    - timestamp1: the time the image was first received.
    - timestamp2: the time the image was ended.

    - x2: the x2 amount the image was upscaled with
    - noise: the noise amount the image was upscaled with
    - model: the model the image was upscaled with

    - is_admin_flagged: whether the image is flagged as Tos breaking by an admin.
    - errors: a dict of errors that occured while creating the image.
    
    Methods:

    - __init__: initialiser for the image class.
    - __str__: returns a string representation of the image.

    - __load: loads the image from the database.
    - __save: saves the image to the database.
    - __pack: packs the image into a dict (for database storage).

    - Async chev_upload: uploads the image to chevereto. (can be used twice, automatically updates the links)
    - Async bigjpg_upload: uploads the image to bigjpg.
    - Async bigjpg_download: downloads the image from bigjpg.

    - end_image: ends the image and saves everything to database.


    """
    def __init__(self,**kwargs) -> None:
        """
        Initialiser for the image class.
        Accepted keyword arguments:
        - uid: The user id of the user who uploaded the image. (must be used with url)
        - url: The url of the image. (must be used with uid)

        - id: The id of the image. (may not be used with uid & url)
        """
        # set default values
        self.uid = None
        self.url = None
        self.id = None
        self.chev1 = None
        self.chev2 = None
        self.chev1r = None
        self.chev2r = None
        self._rayid = None
        self.timestamp1 = None
        self.timestamp2 = None
        self.x2 = None
        self.noise = None
        self.model = None
        self.is_admin_flagged = False
        self.errors = {}

        #TODO Rewrite the kwargs checking
        #check for length of kwargs
        if len(kwargs) == 0: # if no arguments are given
            raise ValueError("No arguments given")
        elif len(kwargs) >= 3: # if too many arguments are given
            raise ValueError("Too many arguments given")
        
        if len(kwargs) == 1:
            try:
                self.id = kwargs['id']
            except KeyError:
                raise ValueError("if only one argument is given, it must be the id")
        elif len(kwargs) == 2:
            try:
                self.uid = kwargs['uid']
                self.url = kwargs['url']
                self.timestamp = time.time()
            except KeyError:
                raise ValueError("if two arguments are given, they must be uid and url")

        # if an id is passed, load the image from the database
        if self.id is not None:
            self.__load()
        

    def __str__(self) -> str:
        """
        Returns a string representation of the image.
        """
        return "Image: {0}".format(self.id) if self.id is not None else "Image: Not saved yet"


    def __load(self) -> None:
        """
        Loads the image from the database.
        """
        #load the database
        db = TinyDB(__database__)
        table = db.table('images')
        q = Query()

        #get the image from the database
        packed = table.get(q.id == self.id)

        #unpack the image
        self.uid =  packed['uid']
        self.url = packed['url']
        self.id = packed['id']
        self.chev1 = packed['chev1']
        self.chev2 = packed['chev2']
        self.chev1r = packed['chev1r']
        self.chev2r = packed['chev2r']
        self._rayid = packed['rayid']
        self.timestamp1 = packed['timestamp1']
        self.timestamp2 = packed['timestamp2']
        self.x2 = packed['x2']
        self.noise = packed['noise']
        self.model = packed['model']
        self.is_admin_flagged = packed['is_admin_flagged']
        self.errors = packed['errors']


    def __save(self) -> None:
        """
        This method saves the image to the database.
        """
        if self.id is None:
            raise ValueError("Image cannot be saved (no id)")

        db = TinyDB(__database__)
        table = db.table('images')
        q = Query()
        packed_data = self.__pack()
        table.upsert(packed_data, q.id == self.id)


    def __pack(self) -> dict:
        """
        packs every attribute of the image into a dict.
        """
        packed = {
            'uid': self.uid,
            'url': self.url,
            'id': self.id,
            'chev1': self.chev1,
            'chev2': self.chev2,
            'chev1r': self.chev1r,
            'chev2r': self.chev2r,
            'rayid': self._rayid,
            'timestamp1': self.timestamp1,
            'timestamp2': self.timestamp2,
            'x2': self.x2,
            'noise': self.noise,
            'model': self.model,
            'is_admin_flagged': self.is_admin_flagged,
            'errors': self.errors,
        }
        return packed


    async def chev_upload(self) -> None:
        """
        This method will upload to chevereto image1 or image2 under these circumstances:
        image1:
            - image1 is not uploaded yet
        image2:
            - image1 is uploaded
            - image2 is not uploaded yet
            - image has been sent to upscaler
        """
        async def upload_image(url):
            # get API key
            key = apiKeys().chevereto_key
            # load website
            weblink = f'https://skahosting.xyz/c/api/1/upload/?key={key}&source={url}&format=json'

            # get webserver response
            async with aiohttp.ClientSession() as session:
                async with session.get(url=weblink) as resp:
                    # extract result data
                    try:
                        r = await resp.json()
                    except: # in case of Json ContentTypeError
                        r = await resp.read()
                        #r = {'status_code':500}
            #handle the response
            if r['status_code'] == 400:
                """Wrong upload"""
                return {'status':400,'error_code':r['error']['code'],'url':None,'id':None}

            elif r['status_code'] == 200:
                """Correctly uploaded"""
                return {
                        'status':200,
                        'size':int(r['image']['size']) / 1000000,  # divide size by 1 000 000 for mb
                        'width':int(r['image']['width']),
                        'heigth':int(r['image']['height']),
                        'id':r['image']['name'],
                        'url':r['image']['url']
                        }

            else:
                """Unknown error, error 404 will be returned"""
                return {'status':400,'error_code':404,'url': None,'id':None}

        if self.chev1 is None and self.chev2 is None and self._rayid is None:
            self.chev1r = await upload_image(self.url)
            self.chev1 = self.chev1r['url']
            self.id = self.chev1r['id'] or 0
        elif self.chev1 is not None and self.chev2 is None and self._rayid is not None:
            self.chev2r = await upload_image(self.url)
            self.chev2 = self.chev2r['url']
            self.id = self.chev2r['id'] or 0
        else:
            raise ValueError("Image already uploaded")
    

    async def bigjpg_upload(self) -> None:
        # get the api key
        key = apiKeys().bigjpg_key

        # check whether chevereto image 1 is uploaded
        if self.chev1 is None:
            raise ValueError("Chevereto image 1 is not uploaded")
        # check if image has already been sent to upscaler
        if self._rayid is not None:
            print(self._rayid)
            raise ValueError("Image has already been sent to upscaler")

        # check if all upscale parameters are set
        if any([True for i in [self.x2, self.model, self.noise] if i is None]): # if any of the upscale parameters are not set, raise an error
            raise ValueError("Upscale parameters are not set")

        '''
        - style can be 'art', 'photo' which means 'cartoon illustration', 'photo'
        - noise can be '-1', '0', '1', '2', '3' which means 'None', 'Low, 'Medium', 'High', 'Highest'
        - x2 can be '1', '2', '3', '4' which means 2x, 4x, 8x, 16x
        '''
        #  set the form parameters
        form = {
            'style': self.model,
            'noise': self.noise,
            'x2': self.x2,
            'input': self.chev1
        }

        #upload the image to bigjpg
        async with aiohttp.ClientSession() as session:
            async with session.post(url='https://bigjpg.com/api/task/', headers={'X-API-KEY': key}, data={'conf': json.dumps(form)}) as r:
                response = await r.json()

        try:
            self._rayid = response['tid']
        except KeyError:
            raise ValueError("Could not upload image to bigjpg")
  

    async def bigjpg_download(self) -> None:
        # check if a valid rayid is set
        if self._rayid is None:
            raise ValueError("image not uploaded to bigjpg yet")

        # creating the API link
        link = f'https://bigjpg.com/api/task/{self._rayid}'

        # requesting the result data
        async with aiohttp.ClientSession() as session:
            async with session.get(url=link) as r:
                # extract result data
                result_data = await r.json()
                result_data = result_data[self._rayid]
                status = result_data['status']
                url = result_data['url']

        #TODO: Analyse response and set correct parameters
        return {'status': status, 'url': url}


    def end_image(self) -> None:
        self.timestamp2 = time.time()
        self.__save()
        del self # renders the object useless after the image is saved


class apiKeys():
    """
    A class that fetches all the api keys from the env file
    """
    def __init__(self) -> None:
        load_dotenv(find_dotenv())
        self.chevereto_key = getenv('chev_key')
        self.bigjpg_key = getenv('bigjpg')


# testing
if __name__ == "__main__":
    ...
