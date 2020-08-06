class Context():

    def __init__(self, message, bot, db, settings, secrets):
        self.message = message
        self.send = message.channel.send if message is not None else None

        self.bot = bot
        self.db = db
        self.secrets = secrets
        self.settings = settings