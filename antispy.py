"""
Unifier AntiSpy - Data scraper detection plugin for Unifier
Copyright (C) 2024  Green

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from nextcord.ext import commands
import importlib

detector = importlib.import_module('utils.detector')

class AntiSpy(commands.Cog):
    """Extension to scan for scrapers on boot and on user join/leave"""
    
    def __init__(self,bot):
        self.bot = bot
        if not hasattr(self.bot,'detector'):
            self.bot.detector = detector.Detector(bot=self.bot)
            self.bot.detector.scanall()
            self.bot.loaded_plugins['antispy'].attach_detector(self.bot.detector)

    @commands.Cog.listener()
    async def on_member_join(self,member):
        await self.bot.loop.run_in_executor(None,lambda:self.bot.detector.check(member))

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        await self.bot.loop.run_in_executor(None, lambda: self.bot.detector.scan(member.guild))

    @commands.command(hidden=True)
    async def refresh_detector(self,ctx):
        importlib.reload(detector)
        self.bot.detector = detector.Detector(bot=self.bot)
        self.bot.detector.scanall()
        self.bot.loaded_plugins['antispy'].attach_detector(self.bot.detector)
        await ctx.send('Refreshed scraper detector')

def setup(bot):
    bot.add_cog(AntiSpy(bot))
