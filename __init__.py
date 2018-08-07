# Copyright 2018 Mycroft AI, Inc.
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
from mycroft.skills.core import FallbackSkill
from mycroft.util import resolve_resource_file

from os.path import join, exists


class StopSkill(FallbackSkill):
    def __init__(self):
        super(StopSkill, self).__init__()
        self.is_match_cache = {}

    def initialize(self):
        self.register_fallback(self.handle_fallback, 50)

    def is_match(self, utt, voc_filename, lang=None):
        """ Determine if the given utterance contains the vocabular proviced

        This checks for vocabulary match in the utternce instead of the other
        way around to allow the user to say things like "yes, please" and
        still match against voc files with only "yes" in it. The method first
        checks in the current skills voc files and secondly in the "text"
        folder in mycroft-core. The result is cached for future uses.

        Args:
            utt (str): Utterance to be tested
            voc_filename (str): Name of vocabulary file (e.g. 'yes' for
                                'res/text/en-us/yes.voc')
            lang (str): Language code, defaults to self.long

        Returns:
            bool: True if the utterance has the given vocabulary it
        """
        lang = lang or self.lang
        if voc_filename not in self.is_match_cache:
            # Check both skill/vocab/LANG and .../res/text/LANG
            voc = join(self.vocab_dir, voc_filename + '.voc')
            if not exists(voc):
                voc = resolve_resource_file(join('text', lang,
                                                 voc_filename + '.voc'))

            if not exists(voc):
                raise FileNotFoundError(
                        'Could not find voc file, checked {} and {}'.format(voc,
                            skill_voc))

            with open(voc) as f:
                self.is_match_cache[voc_filename] = f.read().splitlines()

        # Check for match
        if utt and any(i.strip() in utt
                       for i in self.is_match_cache[voc_filename]):
            return True
        return False


    def handle_fallback(self, message):
        utterance = message.data.get("utterance", "")
        if self.is_match(utterance, 'StopKeyword', self.lang):
            self.emitter.emit(message.reply("mycroft.stop", {}))
            return True
        return False


def create_skill():
    return StopSkill()
