# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.
from os.path import join
from mycroft.skills.core import FallbackSkill
from mycroft.dialog import get_all_vocab


class StopSkill(FallbackSkill):
    def __init__(self):
        super(StopSkill, self).__init__()

    def initialize(self):
        self.register_fallback(self.handle_fallback, 50)
        self.stop_words = get_all_vocab("StopKeyword", self.lang)
        
    def handle_fallback(self, message):
        utterance = message.data.get("utterance", "")
        words = utterance.split(" ")
        for stop_word in self.stop_words:
            if stop_word in words:
                self.emitter.emit(message.reply("mycroft.stop"))
                return True
        return False


def create_skill():
    return StopSkill()
