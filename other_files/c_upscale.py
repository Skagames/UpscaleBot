from models import image as image_class
from models import user as user_class
from other_files import logging, embeds
import asyncio
import time


def fetch_details(x2, noise, model):
    """return the correct definitions of the parameters"""
    # decode the settings to be used in the API
    match x2:
        case None: x2 = 1
        case '2x': x2 = 1
        case '4x': x2 = 2
        case '8x': x2 = 3
        case '16x': x2 = 4
    match noise:
        case None: noise = 0
        case 'None': noise = -1
        case 'Low': noise = 0
        case 'Medium': noise = 1
        case 'High': noise = 2
        case 'Highest': noise = 3
    match model:
        case None: model = 'art'
        case 'Art': model = 'art'
        case 'Photo': model = 'photo'
    
    return {'x2':x2,'noise':noise,'model':model}

async def upscale(ctx, image, x2, noise, model):
    """Upscale your images"""

    msg = await ctx.respond(embed=embeds.upscaleEmbeds().processing(),ephemeral=False)

    # fetch the user
    user = user_class.user(uid=ctx.author.id)
    user.take_image() # removes one image from the user
    user.last_seen = time.time() // 1 # sets the last_seen time of the user to now.

    # check if the user is banned
    """
    Bans are an overarching flag, it is more important than any other flag.
    """
    flags = user.fetch_flags()
    if 0 in flags or 1 in flags: 
        await msg.edit_original_message(embed=embeds.upscaleEmbeds().userbanned(user.uid))
        logging.log(f"{user.uid} used upscale command but was banned")
        user.refund_image()
        user.end_user()

        return
    
    # check if the user has upscales left
    if user.free_images < 0 and 3 not in user.fetch_flags(): # 3 in the flags is permanently free
        await msg.edit_original_message(embed= embeds.upscaleEmbeds().no_upscales_left())
        logging.log(f"{user.uid} used upscale command but has no upscales left")
        user.refund_image()
        user.end_user()
        return

    # initiate an image
    img = image_class.image(url=image, uid = ctx.author.id)
    details = fetch_details(x2, noise, model)
    img.x2 = details['x2']
    img.noise = details['noise']
    img.model = details['model']

    # upload to chev
    await img.chev_upload()
    # check for errors
    if img.chev1 == None:
        await msg.edit_original_message(embed = embeds.upscaleEmbeds().upscale_api_error(user.uid))
        logging.log(f"{user.uid} used upscale command but the API returned an error")
        user.refund_image()
        user.end_user()
        img.end_image()
        return

    # upload to bigjpg
    await img.bigjpg_upload()

    # change embed
    await msg.edit_original_message(embed = embeds.upscaleEmbeds().upscale_progress(img._rayid, user.uid))

    # start waiting for the image to be processed
    while True:
        await asyncio.sleep(15)
        results = await img.bigjpg_download()
        if results['status'] == 'success':
            img.url = results['url']
            break
        elif results['status'] == 'error':
            msg.edit_original_message(embed = embeds.upscaleEmbeds().upscale_api_error(user.uid))
            logging.log(f"{user.uid} used upscale command but the API returned an error")
            user.refund_image()
            user.end_user()
            img.end_image()
            return
        else:
            continue

    # upload the image to chev
    await img.chev_upload()
    # check for errors
    if img.chev2 == None:
        await msg.edit_original_message(embed = embeds.upscaleEmbeds().upscale_api_error(user.uid))
        logging.log(f"{user.uid} used upscale command but the API returned an error")
        user.refund_image()
        user.end_user()
        img.end_image()
        return

    # send image to discord
    await msg.edit_original_message(embed= embeds.upscaleEmbeds().upscale_success(img.chev2, img._rayid, user.uid, user.free_images))

    # log the image
    logging.log(f"{user.uid} used upscale command and upscaled: {img.chev2}")

    # add an image to the total upscaled images
    user.total_images += 1
    user.images.append(img.id)
    user.end_user()
    img.end_image()
    return