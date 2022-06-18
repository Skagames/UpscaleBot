import discord

class helpEmbed():
    def __init__(self,version):
        self.embed = None
        self.version = version

    def helpV1(self):
        text = f"""
`UpscaleBot V{self.version}`
>>> -------------------------
UpscaleBot is a bot that can upscale images.
It can upscale images to 2x, 4x, 8x, 16x, and can also upscale images with noise reduction.
-------------------------
**Commands**
*arguments in [] are required, <> are optional*
1) /help -> you are here
2) /ping -> get bot ping and basic info
3) /upscale [image] <amount> <noise> <model>
    - image: The image you want to upscale
    - amount: The amount of times you want to upscale (8x and 16x might not work)
    - noise: How much noise reduction the upscale should have
    - model: Which upscaling model to use (art for drawings/anime, photo for irl images)"""
        return text


async def help(ctx,version):
    h = helpEmbed(version)
    await ctx.respond(h.helpV1())