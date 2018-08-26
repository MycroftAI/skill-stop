# Copyright 2016 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from adapt.intent import IntentBuilder

from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill

__author__ = 'jdorleans'


class StopSkill(MycroftSkill):
    def __init__(self):
        super(StopSkill, self).__init__(name="StopSkill")

    def initialize(self):
        # TODO - To be generalized in MycroftSkill
        intent = IntentBuilder("StopIntent").require("StopKeyword").build()
        self.register_intent(intent, self.handle_intent)

    def handle_intent(self, event):
        self.bus.emit(Message("mycroft.stop"))

    def stop(self):
        pass


def create_skill():
    return StopSkill()
