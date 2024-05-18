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

import discord
import revolt
import guilded
from detector import Detector

detector = Detector() # this is solely to make pycharm stop complaining

async def attach_detector(detector_obj):
    global detector
    detector: Detector = detector_obj

async def scan(message: discord.Message or revolt.Message or guilded.Message, data):
    global detector

    response = {
        'unsafe': False,
        'description': 'No suspicious content found',
        'target': {},
        'delete': [],
        'restrict': {},
        'data': {},
        'public': True
    }

    if not detector.bot:
        try:
            detector = data['detector']
        except:
            pass

    if detector.bot:
        if message.guild.id in detector.infected.keys():
            scraperlist = ''
            for scraper in detector.infected[message.guild.id]:
                if len(scraperlist)==0:
                    scraperlist = f'- <@{scraper}>'
                else:
                    scraperlist = scraperlist + f'\n- <@{scraper}>'
            response['unsafe'] = True
            response['description'] = (
                    'One or more scraper bots were detected in your server. Please ask your server moderators to'+
                    'remove them immediately.\n'+scraperlist+'\n\nSource: kickthespy.pet'
            )

    response['data'] = {'detector':detector}
    return response
