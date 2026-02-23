import os
import json
from supybot import callbacks, conf, log, ircdb, ircmsgs
from supybot.commands import wrap

class TildeChat(callbacks.Plugin):
    """
    Tilde.chat compliance module. 
    Automates +B user mode and handles mandatory !botlist and !rollcall triggers.
    """

    def __init__(self, irc):
        super().__init__(irc)
        self.db_path = os.path.join(conf.supybot.directories.data(), 'TildeChat.json')
        self.settings = self._load_db()

    def _load_db(self):
        """Loads settings from JSON or returns generic defaults."""
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return {
            "enabled_networks": [],
            "botlist": "Maintainer: [set with 'tc set botlist <text>'] | IRC Bot | Commands: !help",
            "rollcall": "IRC Bot reporting in! Use !help for commands."
        }

    def _save_db(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def _apply_bot_mode(self, irc):
        """Immediately sends MODE +B to the current network."""
        irc.queueMsg(ircmsgs.mode(irc.nick, '+B'))
        log.info(f"TildeChat: Sent MODE +B to {irc.network}")

    def _update_network_config(self, network_name):
        """Updates Limnoria's registry to ensure +B is set on every reconnect."""
        try:
            network_conf = conf.supybot.networks.get(network_name)
            current_modes = network_conf.userModes()
            if 'B' not in current_modes:
                new_modes = current_modes + 'B' if '+' in current_modes else '+B'
                network_conf.userModes.setValue(new_modes)
                log.info(f"TildeChat: Updated config userModes for {network_name}")
                return True
        except Exception as e:
            log.error(f"TildeChat: Failed to update config for {network_name}: {e}")
        return False

    def doPrivmsg(self, irc, msg):
        """
        Intercepts !botlist and !rollcall ONLY if '!' is NOT 
        the bot's primary command prefix.
        """
        if irc.network not in self.settings.get("enabled_networks", []):
            return
        
        # If '!' is a valid prefix, Limnoria handles this via regular commands
        if "!" in conf.supybot.reply.prefixes():
            return

        channel = msg.args[0]
        text = msg.args[1].strip().lower()

        if text == "!botlist":
            irc.sendMsg(ircmsgs.privmsg(channel, self.settings["botlist"]))
        elif text == "!rollcall":
            irc.sendMsg(ircmsgs.privmsg(channel, self.settings["rollcall"]))

    def botlist(self, irc, msg, args):
        """takes no arguments.
        Returns the tilde.chat botlist compliance string.
        """
        if irc.network not in self.settings.get("enabled_networks", []):
            return
        irc.reply(self.settings["botlist"], prefixNick=False)
    botlist = wrap(botlist)

    def rollcall(self, irc, msg, args):
        """takes no arguments.
        Returns the tilde.chat rollcall compliance string.
        """
        if irc.network not in self.settings.get("enabled_networks", []):
            return
        irc.reply(self.settings["rollcall"], prefixNick=False)
    rollcall = wrap(rollcall)

    def tchenable(self, irc, msg, args):
        """takes no arguments.
        Enable tilde.chat compliance and set +B mode for this network.
        """
        if not ircdb.checkCapability(msg.prefix, 'admin'):
            irc.error("Admin capability required.")
            return
        
        net = irc.network
        self._apply_bot_mode(irc)
        self._update_network_config(net)
        
        if net not in self.settings["enabled_networks"]:
            self.settings["enabled_networks"].append(net)
            self._save_db()
            irc.reply(f"Tilde.chat compliance enabled for {net}.")
    enable = wrap(tchenable)

    def tcdisable(self, irc, msg, args):
        """takes no arguments.
        Disable tilde.chat compliance for this network.
        """
        if not ircdb.checkCapability(msg.prefix, 'admin'):
            irc.error("Admin capability required.")
            return
        net = irc.network
        if net in self.settings["enabled_networks"]:
            self.settings["enabled_networks"].remove(net)
            self._save_db()
            irc.reply(f"Tilde.chat compliance disabled for {net}.")
    disable = wrap(tcdisable)

    def tcset(self, irc, msg, args, type, response):
        """<botlist|rollcall> <text>
        Sets the response string for the specified trigger.
        """
        if not ircdb.checkCapability(msg.prefix, 'admin'):
            irc.error("Admin capability required.")
            return
        key = type.lower()
        if key not in ['botlist', 'rollcall']:
            irc.error("Type must be 'botlist' or 'rollcall'")
            return
        self.settings[key] = response
        self._save_db()
        irc.replySuccess()
    set = wrap(tcset, ['somethingWithoutSpaces', 'text'])

Class = TildeChat