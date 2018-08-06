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
from os.path import join
from mycroft.skills.core import FallbackSkill
from mycroft.util import resolve_resource_file


def get_all_vocab(phrase, lang=None, vocab_path=None):
    """
    Looks up a resource file for the given phrase.  If no file
    is found, the requested phrase is returned as the string.
    This will use the default language for translations.

    Args:
        phrase (str): resource phrase to retrieve/translate
        lang (str): the language to use

    Returns:
        phrases (list): a list with all versions of the phrase
    """
    if not lang:
        from mycroft.configuration import Configuration
        lang = Configuration.get().get("lang", "en-us")

    if ".voc" not in phrase:
        phrase += ".voc"

    voc_filename = join(vocab_path, lang.lower(), phrase + '.voc')
    template = resolve_resource_file(voc_filename)

    if template:
        with open(template) as f:
            phrases = list(filter(bool, f.read().split('\n')))

    elif vocab_path is not None:
        voc_filename = join(vocab_path, phrase)
        template = resolve_resource_file(voc_filename)
        if template:
            with open(template) as f:
                phrases = list(filter(bool, f.read().split('\n')))

    if not template:
        LOG.debug("Resource file not found: " + voc_filename)
        phrases = [phrase]

    return phrases


class StopSkill(FallbackSkill):
    def __init__(self):
        super(StopSkill, self).__init__()

    def initialize(self):
        self.register_fallback(self.handle_fallback, 50)
        self.stop_words = get_all_vocab("StopKeyword", self.lang,
                                        self.vocab_dir)

    def handle_fallback(self, message):
        utterance = message.data.get("utterance", "")
        for stop_word in self.stop_words:
            if stop_word in utterance:
                self.emitter.emit(message.reply("mycroft.stop", {}))
                return True
        return False


def create_skill():
    return StopSkill()
