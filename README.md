# dismusic-slash

Music extension making use of discord.py v2.1. Supports YouTube, YoutubeMusic, SoundCloud and Spotify.

# Notice

This project is for my personal use and work as I intend it to. I will not add any features to it. I will be only fixing errors or updating it as discord.py updates.

# Installation

From Github

```sh
python3 -m pip install git+https://github.com/Ewxun/dismusic-slash.git
```

# Usage

```python
from discord.ext import commands

bot = commands.Bot(command_prefix='..')

bot.lavalink_nodes = [
    {"host": "losingtime.dpaste.org", "port": 2124, "password": "SleepingOnTrains"},
    # Can have multiple nodes here
]

# If you want to use spotify search
bot.spotify_credentials = {
    'client_id': 'CLIENT_ID_HERE',
    'client_secret': 'CLIENT_SECRET_HERE'
}

# If you want your slash commands to be grouped under `music` set to True (Default: True)
bot.music_prefixed = True


bot.load_extension('dismusic-slash')
bot.run('TOKEN')
```

# Commands

**connect** - `Connect to vc` \
**disconnect** - `Disconnect from vc`

**play** - `Play a song or playlist` \
**pause** - `Pause player` \
**resume** - `Resume player`

**seek** - `Seek player` \
**nowplaying** - `Now playing` \
**queue** - `See queue` \
**volume** - `Set volume` \
**loop** - `Loop song/playlist`

# Events

Events that this library dispatches

```py
on_dismusic_player_connect(player):
    # When player connects to a voice channel

on_dismusic_player_stop(player):
    # When player gets disconnected

on_dismusic_track_start(player, track):
    # When a song start playing

on_dismusic_track_end(player, track):
    # When a song finished

on_dismusic_track_exception(player, track):
    # When song stops due to any exception

on_dismusic_track_stuck(player, track):
    # When a song gets stuck

on_dismusic_player_pause(player):
    # When player gets paused

on_dismusic_player_resume(player):
    # When player gets resumed

on_dismusic_player_seek(player, previous_position, current_position):
    # When player seeks
```

# Lavalink Configs
Find configs here [https://lavalink.darrennathanael.com/](https://lavalink.darrennathanael.com/)

DM `Ewxun#6311` For any kind of help
