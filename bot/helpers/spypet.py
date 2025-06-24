class Spypet:
    def __init__(self):
        self.bot = None
        self.messages = {}

    def set_bot(self, bot):
        self.bot = bot

    def add_message(self, guild, channel, message):
        if guild.name not in self.messages:
            self.messages[guild.name] = {}
        if channel.name not in self.messages[guild.name]:
            self.messages[guild.name][channel.name] = []
        self.messages[guild.name][channel.name].append(message)

    def clear_messages(self):
        self.messages = {} 