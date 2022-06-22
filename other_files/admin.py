"""
This file is for the admin commands.
"""
from tinydb import TinyDB, Query
import discord
from other_files import logging

def is_admin(uid):
    """
    Check if the user is an admin.
    """
    db = TinyDB('db.json')
    table = db.table('users')
    query = Query()
    packed = table.get(query.uid == uid)
    if packed is None:
        return False
    if packed['user_flags'] & (1 << 5) == 1 << 5:
        return True

async def change_flags(ctx, user, new_flag_value):
    """
    Change the flags of a user.
    """
    if not is_admin(ctx.author.id):
        await ctx.respond("You are not an admin.")
        logging.log(f"{ctx.author.id} tried to change flags of {user} but failed (perms).")
        return
    user = int(user)

    if type(user) is not int:
        await ctx.respond("The user ID must be an integer.")
        logging.log(f"{ctx.author.id} tried to change flags of {user} but failed (wrong int).")
        return
    
    db = TinyDB('db.json')
    table = db.table('users')
    query = Query()

    table.upsert({'user_flags': new_flag_value}, query.uid == user)
    await ctx.respond(f"User {user}'s flags have been changed to {new_flag_value}.")
    logging.log(f"{ctx.author.id} changed flags of {user} to {new_flag_value}.")
    

async def calculate_flag_value(ctx, flags = None, flag_list = None):
    """
    Calculate the flag value of a user.
    """
    # check if user is an admin
    if not is_admin(ctx.author.id):
        await ctx.respond("You are not an admin.")
        logging.log(f"{ctx.author.id} tried to calculate flag value but failed (perms).")
        return
    
    # convert flags to bool
    flag_list = True if flag_list == 'True' else False


    FLAGTEXT = """- user_flags: integer representing the flags of the user.
        - None: user does not have any flags.
        - 0: user is permanently banned
        - 1: user is temporarily banned
        - 2: user has unlocked premium features
        - 3: user has permanent premium & upscales [courtesy of the admins]
        - 4: user has been previously banned
        - 5: is admin user
        - 6: has beta permissions
        - 1 << 7-16: reserved for future use """

    if flags is not None:
        flags = flags.split(",")
        total = str(sum([1 << int(flag) for flag in flags]))

    text = ''
    if flag_list is not None:
        text += FLAGTEXT + "\n\n"
    if flags is not None:
        text += f"Flag value: {total} (from flags: {', '.join(flags)})"

    await ctx.respond(text)
    logging.log(f"{ctx.author.id} calculated flag value.")

async def fetch_logs(ctx):
    """
    Fetches the latest user-logs and sends them to the user ephemerally.
    """

    # check if user is admin
    if not is_admin(ctx.author.id):
        await ctx.respond("You are not an admin.")
        return

    await ctx.respond(content='Fetched latest db',file=discord.File('db.json'),ephemeral=True)
    logging.log(f"{ctx.author.id} fetched logs.")
    
