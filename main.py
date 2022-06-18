import discord
from discord import interactions
from discord.ext import commands
from discord.interactions import Interaction
import random
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from io import BytesIO
from config.server import keep_alive
import os


bot = commands.Bot()


class aarrModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            "AARRアイコン認証"
        )
        self.num = random.choice(range(0,10))
        self.num2 = random.choice(range(0,10))
        self.mondai = discord.ui.InputText(
            label=f"{self.num}+{self.num2}は？",
            style=discord.InputTextStyle.short,
            placeholder="書いてね",
            required=True,
        )
        self.add_item(self.mondai)
    async def callback(self, interaction: interactions.Interaction) -> None:
        if self.mondai.value == f"{self.num + self.num2}" or self.mondai.value == f"{self.num}{self.num2}":
          user=interaction.user
          userstr = user
          asset = user.avatar
          data = BytesIO(await asset.read())
          img = Image.new("RGB", (1280, 1280), (128, 128, 128))
          user = Image.open(data).convert("RGBA").resize((910,900))
          aarr = Image.open("config/aarr.png").convert("RGBA").resize((1280,1280))
          img.paste(user, (180, 210), user)
          img.paste(aarr, (0, 0), aarr)
          img.save("config/slashusericon.png")
          await interaction.response.send_message(f"{userstr}さんのアイコン画像です",file=discord.File("config/slashusericon.png"),ephemeral=True)
          return
        if not self.mondai.value == f"{self.num + self.num2}" or self.mondai.value == f"{self.num}{self.num2}":
          await interaction.response.send_message("あってない",ephemeral=True)
          return
        return



@bot.slash_command(name="aarricongen", description="AARRのアイコンフレーム付きアイコンを作ります")
async def icon_slash(interaction: Interaction):
    modal = aarrModal()
    await interaction.response.send_modal(modal=modal)


keep_alive()
bot.run(os.getenv("TOKEN"))
