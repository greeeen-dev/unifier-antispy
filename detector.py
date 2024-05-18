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

import requests
import json

debug = False # if true, adds green's alt as a scraper

class Detector:
    def __init__(self,bot=None,data=None):
        if not data:
            try:
                data = requests.get('https://kickthespy.pet/ids').json()
                if not type(data) is list:
                    raise ValueError()
            except:
                with open('spypet_backup.json') as file:
                    data = json.load(file)
                data = data['data']
        self.scrapers = data
        with open('spypet_backup.json', "w+") as file:
            json.dump(self.scrapers, file)
        if debug:
            self.scrapers.append(440119103714361355)
        self.infected = {}
        self.bot = bot

    def scanall(self):
        self.infected = {}
        for guild in self.bot.guilds:
            members = guild.members
            bots = []
            for member in members:
                if member.id in self.scrapers:
                    bots.append(member.id)
            self.infected.update({
                f'{guild.id}': bots
            })

        return len(self.infected.keys()) > 0, self.infected

    def scan(self,guild):
        members = guild.members
        bots = []
        for member in members:
            if member.id in self.scrapers:
                bots.append(member.id)
        if len(bots) > 0:
            self.infected.update({
                f'{guild.id}': bots
            })
        else:
            if f'{guild.id}' in self.infected.keys:
                self.infected.pop(f'{guild.id}')
        return len(bots) > 0, bots

    def check(self,member):
        if member.id in self.scrapers:
            self.scan(member.guild)
            return True
        return False
