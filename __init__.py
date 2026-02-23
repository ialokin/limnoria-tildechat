"""
TildeChat: Compliance module for tilde.chat network standards.
Provides mandatory !botlist and !rollcall responses and makes sure the bot sets mode +B.
"""

import supybot
import supybot.world as world

# Use a version string for tracking updates
__version__ = "2026.02.23"

# Replace with your actual information
__author__ = supybot.Author(name='ialokin', nick='ialokin', email='ialokin@tilde.ninja')
__maintainer__ = __author__
__url__ = 'https://github.com/ialokin/limnoria-tildechat'

from . import config
from . import plugin
from importlib import reload

# Ensure the plugin can be reloaded live in IRC via '@reload TildeChat'
reload(config)
reload(plugin)

if world.testing:
    from . import test

# This tells Limnoria which class to instantiate when the plugin is loaded
Class = plugin.Class
configure = config.configure