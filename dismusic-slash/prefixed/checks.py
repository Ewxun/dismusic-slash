from discord.ext import commands
import discord

from .errors import MustBeSameChannel, NotConnectedToVoice, PlayerNotConnected


def voice_connected():
    def predicate(interaction: discord.Interaction):
        if not interaction.user.voice:
            raise NotConnectedToVoice("You are not connected to any voice channel.")

        return True

    return commands.check(predicate)


def player_connected():
    def predicate(interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            raise PlayerNotConnected("Player is not connected to any voice channel.")

        return True

    return commands.check(predicate)


def in_same_channel():
    def predicate(interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            raise PlayerNotConnected("Player is not connected to any voice channel.")

        if interaction.guild.voice_client.channel.id != interaction.user.voice.channel.id:
            raise MustBeSameChannel("You must be in the same voice channel as the player.")

        return True

    return commands.check(predicate)


def voice_channel_player():
    def predicate(interaction: discord.Interaction):
        if not interaction.user.voice:
            raise NotConnectedToVoice("You are not connected to any voice channel.")

        if not interaction.guild.voice_client:
            raise PlayerNotConnected("Player is not connected to any voice channel.")

        if interaction.guild.voice_client.channel.id != interaction.user.voice.channel.id:
            raise MustBeSameChannel("You must be in the same voice channel as the player.")

        return True

    return commands.check(predicate)
