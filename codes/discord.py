from pypresence import Presence
import time
class DiscordStat:
    def __init__(self, mapName):
        start = int(time.time())
        try:
            pass
            client_id = "1224296426432102442"  # your application's client id
            RPC = Presence(client_id)
            RPC.connect()
        except:
            pass

        def discordState(mapName):
            RPC.update(
                large_image="distormium",  # name of your asset
                large_text="distormium",
                details="The game is in development.",
                state=f"On '{mapName}'",
                start=start
            )

        discordState(mapName)