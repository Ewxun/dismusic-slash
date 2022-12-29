"""Copyright 2022 Ewxun

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from ._version import __version__, version_info


async def setup(bot):
    try:
        f = str(bot.music_prefixed)
    except:
        bot.music_prefixed = True
    if bot.music_prefixed:
        from .prefixed.events import MusicEvents_v2
        from .prefixed.music_v2 import Music_v2
        await bot.add_cog(Music_v2(bot))
        await bot.add_cog(MusicEvents_v2(bot))
    else:
        from .non_prefixed.events import MusicEvents_v2
        from .non_prefixed.music_v2 import Music_v2
        await bot.add_cog(Music_v2(bot))
        await bot.add_cog(MusicEvents_v2(bot))
