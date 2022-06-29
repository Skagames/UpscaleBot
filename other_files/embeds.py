import discord
from other_files import version
__version__ = version.version

class upscaleEmbeds():
    """
    Embeds for the upscaling command
    """
    def __init__(self):
        pass

    def processing(self):
        embed = discord.Embed(title="Processing...", description="", color=0xad00cc)
        embed.set_footer(text=f"UpscaleBot V{__version__}")
        return embed

    def userbanned(self,uid):
        title = 'You are Banned!'
        description = '<@' + str(uid) + '> ' + 'You\'ve been banned for violating the ToS (Terms of Service)\nOur mods found that your image does not comply with the ToS of discord and you are no longer allowed to upscale images'
        embed=discord.Embed(title=title, description=description, color=0xff0000)
        embed.set_thumbnail(url="https://skahosting.xyz/c/images/BxF2.png")
        embed.add_field(name="Ban appeals:", value="Users that violate the ToS can apply for an unban [here](https://skahosting.xyz/support).\nIf you've been banned for anything that is deemed illegal by U.S. law you will __***never***__  be granted an unban.", inline=False)
        embed.set_footer(text=f"UpscaleBot V{__version__}")
        return embed

    def no_upscales_left(self):
        title = "You have no free upscales left"
        author =  "Upscale Error :("
        embed=discord.Embed(title=title,description='', color=0xd60000)
        embed.set_author(name=author, icon_url="https://skahosting.xyz/c/images/BxF2.png")
        embed.set_thumbnail(url="https://skahosting.xyz/c/images/Biuw.png")
        embed.add_field(name="You have used all your upscales", value="\nYou can wait until next month to receive 5 new free upscales or buy a premium version to upscale more images in een better quality! If you have questions you can always ask them [here](https://skahosting.xyz/support)", inline=False)
        embed.set_footer(text=f"UpscaleBot V{__version__}")
        return embed
    
    def upscale_api_error(self, uid):
        titledesc = '<@' + str(uid) + '> id: `'
        embed=discord.Embed(title="API ERROR :(", description=titledesc, color=0xc80000)
        embed.set_thumbnail(url="https://skahosting.xyz/c/images/Biuw.png")
        embed.add_field(name="What could've gone wrong?", value='This is *probably* not your fault, there is something wrong with the API currently.', inline=False)
        embed.add_field(name="What to do now :/", value="please try again in a couple hours, the API might be having a lot more traffic than usual, causing upscale errors.", inline=True)
        embed.add_field(name="still failing after waiting?", value="join our support server [here](https://skahosting.xyz/support)", inline=True)
        embed.set_footer(text=f"UpscaleBot V{__version__}")
        return(embed)

    def upscale_progress(self, rayid, uid):
        pinguser = '<@' + str(uid) + '> : We have started your upscale!'
        ray = '`' + rayid + '`'
        embed=discord.Embed(title="Upscale Begun!", description=pinguser, color=0xe8ccff)
        embed.set_thumbnail(url="https://skahosting.xyz/c/images/Biuw.png")
        embed.add_field(name="ID:", value=ray, inline=False)
        embed.add_field(name="Upscale Progress:", value="Upscale is currently in progress, We will update this message when it's done!", inline=False)
        embed.set_footer(text=f"UpscaleBot V{__version__}")
        return(embed)

    def upscale_success(self, link, rayid, uid):
        titledesc = '<@' + str(uid) + '> id: `' + rayid + '`' 
        linked = '[Here](' + link + ')'
        embed=discord.Embed(title="Upscale Success!", description=titledesc,color=0x00c800)
        embed.set_image(url=link)
        embed.set_thumbnail(url="https://skahosting.xyz/c/images/Biuw.png")
        embed.add_field(name="you can download your image", value=linked, inline=False)
        embed.set_footer(text="UpscaleBot by !SKA#0001")
        return(embed)


class helpEmbeds():
    """
    Embeds for the help command
    """
    def __init__(self):
        pass

    def help_embed(self):
        embed=discord.Embed(title=f"Upscale Bot V{__version__}", description="How to use the upscaler?\nArguments in [] are required, <> is optional", color=0xffa800)
        embed.set_thumbnail(url="https://skahosting.xyz/c/images/BnNg.png")
        embed.add_field(name="/help", value="You are currently here!", inline=False)
        embed.add_field(name="/ping", value="Bot ping and changelog", inline=False)
        embed.add_field(name="/upscale <link>",value="This is the main command to upscale images! \
                        \nThe command works like this: /upscale [image] <amount> <noise_reduction> <model> \
                        \n - Image: the image you want to upscale (add as an attachment) \
                        \n - Amount: the amount of times you want to upscale the image \
                        \n - Noise_reduction: The amount of noise reduction you want to apply to the upscaled image \
                        \n - Model: Which model you would like to use for the image",inline=False)
        embed.add_field(name="Need more help?",value="You can join our support server => [here](https://skahosting.xyz/support)",inline=False)
        embed.set_footer(text="UpscaleBot by !SKA#0001")
        return(embed)


class settingsEmbeds():
    def __init__(self) -> None:
        pass

    def show(self,avatar_url,name):
        embed = discord.Embed(title=f"Settings", description="Your current active settings will be displayed here", color=0xffa800)
        embed.set_thumbnail(url=avatar_url)
        embed.add_field(name="", value="")
        return embed