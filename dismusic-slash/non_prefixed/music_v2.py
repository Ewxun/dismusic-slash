import asyncio
import async_timeout
import wavelink
import discord
from discord import ClientException, Color, Embed
from discord import app_commands
from discord.ext import commands
from wavelink import LavalinkException, LoadTrackError, SoundCloudTrack, YouTubeMusicTrack, YouTubeTrack
from wavelink.ext import spotify
from wavelink.ext.spotify import SpotifyTrack

from ._classes import Provider
from .checks import voice_channel_player, voice_connected
from .errors import MustBeSameChannel
from .player import DisPlayer

class Music_v2(commands.Cog):
    """Music commands"""

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.bot.loop.create_task(self.start_nodes())

    async def play_track(self, interaction: discord.Interaction, query: str, provider=None):
        player: DisPlayer = interaction.guild.voice_client

        if interaction.user.voice.channel.id != player.channel.id:
            raise MustBeSameChannel("**You must be in the same voice channel as the player.**")

        track_provider = {
            "yt": YouTubeTrack,
            "ytmusic": YouTubeMusicTrack,
            "soundcloud": SoundCloudTrack,
            "spotify": SpotifyTrack,
        }

        msg = await interaction.channel.send(f"**Searching for** `{query}` :mag_right:")

        provider: Provider = (
            track_provider.get(provider) if provider else track_provider.get(player.track_provider)
        )
        nodes = wavelink.NodePool._nodes.values()

        for node in nodes:
            tracks = []
            try:
                with async_timeout.timeout(20):
                    tracks = await provider.search(query, node=node)
                    break
            except asyncio.TimeoutError:
                self.bot.dispatch("dismusic_node_fail", node)
                continue
            except (LavalinkException, LoadTrackError):
                continue

        if not tracks:
            return await interaction.response.send_message("**No song/track found with given query.**")

        track = tracks[0]

        await interaction.channel.send(f"**Added** `{track.title}` **to queue.** ")
        await player.queue.put(track)

        if not player.is_playing():
            await player.do_next()

    async def start_nodes(self):
        await self.bot.wait_until_ready()
        spotify_credential = getattr(self.bot, "spotify_credentials", {"client_id": "", "client_secret": ""})

        for config in self.bot.lavalink_nodes:
            try:
                node: wavelink.Node = await wavelink.NodePool.create_node(
                    bot=self.bot, **config, spotify_client=spotify.SpotifyClient(**spotify_credential)
                )
                print(f"[music-cord] INFO - Created node: {node.identifier}")
            except Exception:
                print(f"[music-cord] ERROR - Failed to create node {config['host']}:{config['port']}")

    @app_command.command()
    @voice_connected()
    async def connect(self, interaction: discord.Interaction):
        """Connect the player"""
        if interaction.guild.voice_client:
            return

        await interaction.response.send_message(f"**Connecting to **`{ctx.author.voice.channel}`")

        try:
            player: DisPlayer = await interaction
user.voice.channel.connect(cls=DisPlayer)
            self.bot.dispatch("dismusic_player_connect", player)
        except (asyncio.TimeoutError, ClientException):
            await interaction.response.send_message("**Failed to connect to voice channel.**")

        player.bound_channel = ctx.channel
        player.bot = self.bot

        await interaction.response.edit_message(content=f"**Connected to **`{player.channel.name}`")
        
        
    @app_command.command()
    @voice_channel_player()
    async def volume(self, interaction: discord.Interaction, vol: int, forced:bool=False):
        """Set volume"""
        player: DisPlayer = interaction.guild.voice_client

        if vol < 0:
            return await interaction.response.send_message("**Volume can't be less than 0**")

        if vol > 100 and not forced:
            return await interaction.response.send_message("**Volume can't greater than 100**")

        await player.set_volume(vol)
        await interaction.response.send_message(f"**Volume set to** {vol} :loud_sound:")
        
    @app_command.command()
    @voice_connected()
    async def play(self, interaction: discord.Interaction, *, query: str):
        """Play or add song to queue (Defaults to YouTube)"""
        if interaction.guild.voice_client:
            pass
        else:
          await interaction.response.send_message(f"**Connecting to **`{ctx.user.voice.channel}`")

          try:
            player: DisPlayer = await interaction.user.voice.channel.connect(cls=DisPlayer)
            self.bot.dispatch("dismusic_player_connect", player)
          except (asyncio.TimeoutError, ClientException):
            await interaction.response.edit_message("**Failed to connect to voice channel.**")

          player.bound_channel = interaction.channel
          player.bot = self.bot

          await interaction.response.edit_message(content=f"**Connected to **`{player.channel.name}`")
        await self.play_track(interaction, query)
        
    @app_command.command()
    @voice_connected()
    async def alwaysjoined(self, interaction: discord.Interaction):
        """Enable 24/7 to disable it just do /music stop"""
        if interaction.guild.voice_client:
            return await interaction.response.send_message("Already enabled to disable it do /stop")

        await interaction.response.send_message(f"**Enabling 24/7 in **`{ctx.author.voice.channel}`!")

        try:
            player: DisPlayer = await interaction.user.voice.channel.connect(cls=DisPlayer)
            self.bot.dispatch("dismusic_player_connect", player)
        except (asyncio.TimeoutError, ClientException):
            await interaction.response.edit_message("**Failed to enable!**")

        player.bound_channel = interaction.channel
        player.bot = self.bot

        await interaction.response.edit_message(content=f"**Enabled 24/7 in **`{player.channel.name}`!")

    @app_command.command()
    @voice_channel_player()
    async def stop(self, interaction: discord.Interaction):
        """Stop the player"""
        player: DisPlayer = interaction.guild.voice_client

        await player.destroy()
        await interaction.response.send_message("**Stopped the player** :stop_button: ")
        self.bot.dispatch("dismusic_player_stop", player)

    @app_command.command()
    @voice_channel_player()
    async def pause(self, interaction: discord.Interaction):
        """Pause the player"""
        player: DisPlayer = interaction.guild.voice_client

        if player.is_playing():
            if player.is_paused():
                return await interaction.response.send_message("**Player is already paused**.")

            await player.set_pause(pause=True)
            self.bot.dispatch("dismusic_player_pause", player)
            return await interaction.response.send_message("**Paused** :pause_button: ")

        await interaction.response.send_message("**Player is not playing anything.**")

    @app_command.command()
    @voice_channel_player()
    async def resume(self, interaction: discord.Interaction):
        """Resume the player"""
        player: DisPlayer = interaction.guild.voice_client

        if player.is_playing():
            if not player.is_paused():
                return await interaction.response.send_message("**Player is already playing.**")

            await player.set_pause(pause=False)
            self.bot.dispatch("dismusic_player_resume", player)
            return await interaction.response.send_message("**Resumed** :musical_note: ")

        await interaction.response.send_message("**Player is not playing anything.**")

    @app_command.command()
    @voice_channel_player()
    async def skip(self, interaction: discord.Interaction):
        """Skip to next song in the queue."""
        player: DisPlayer = interaction.guild.voice_client

        if player.loop == "CURRENT":
            player.loop = "NONE"

        await player.stop()

        self.bot.dispatch("dismusic_track_skip", player)
        await interaction.response.send_message("**Skipped** :track_next:")

    @app_command.command()
    @voice_channel_player()
    async def seek(self, interaction: discord.Interaction, seconds: int):
        """Seek the player backward or forward"""
        player: DisPlayer = interaction.guild.voice_client

        if player.is_playing():
            old_position = player.position
            position = old_position + seconds
            if position > player.source.length:
                return await interaction.response.send_message("**Can't seek past the end of the track.**")

            if position < 0:
                position = 0

            await player.seek(position * 1000)
            self.bot.dispatch("dismusic_player_seek", player, old_position, position)
            return await interaction.response.send_message(f"**Seeked {seconds} seconds** :fast_forward: ")

        await interaction.response.send_message("**Player is not playing anything.**")

    @app_command.command()
    @voice_channel_player()
    async def loop(self, ctx: commands.Context, loop_type: str = None):
        """Set loop to `NONE`, `CURRENT` or `PLAYLIST`"""
        player: DisPlayer = interaction.guild.voice_client

        result = await player.set_loop(loop_type)
        await interaction.response.send_message(f"Loop has been set to {result} :repeat: ")

    @app_command.command()
    @voice_channel_player()
    async def queue(self, interaction: discord.Interaction):
        """Player queue"""
        player: DisPlayer = interaction.guild.voice_client

        if len(player.queue._queue) < 1:
            return await interaction.response.send_message("**Nothing is in the queue.**")

        embed = Embed(color=Color(0x2F3136))
        embed.set_author(
            name="Queue",
            icon_url="https://cdn.discordapp.com/attachments/776345413132877854/940247400046542948/list.png",
        )

        tracks = ""
        length = 0

        if player.loop == "CURRENT":
            next_song = f"Next > [{player.source.title}]({player.source.uri}) \n\n"
        else:
            next_song = ""

        if next_song:
            tracks += next_song

        for index, track in enumerate(player.queue._queue):
            tracks += f"{index + 1}. [{track.title}]({track.uri}) \n"
            length += track.length

        embed.description = tracks

        if length > 3600:
            length = f"{int(length // 3600)}h {int(length % 3600 // 60)}m {int(length % 60)}s"
        elif length > 60:
            length = f"{int(length // 60)}m {int(length % 60)}s"
        else:
            length = f"{int(length)}s"

        embed.set_footer(text=length)

        await interaction.response.send_message(embed=embed)

    @app_command.command()
    @voice_channel_player()
    async def nowplaying(self, interaction: discord.Interaction):
        """Currently playing song information"""
        player: DisPlayer = interaction.guild.voice_client
        await player.invoke_player(interaction, True)
