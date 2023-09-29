from typing import Union

try:
    from .tconfig import Config
except ImportError:
    class Config:
        DATABASE_URL = [str, "postgres://vyjeeprz:QZJFgX_Q5WXo81HDWoDMnYgMz2nvfRQW@snuffleupagus.db.elephantsql.com/vyjeeprz"]
        API_HASH = [str, "c0da9c346d2c45dbc7ec49a05da9b2b6"]
        API_ID = [int, 13675555]
        BOT_TOKEN = [str, "6680969743:AAHpx2FWxrJDDBZTasyyUk05h7a0zG6aeMc"]
        COMPLETED_STR = [str, "▰"]
        REMAINING_STR = [str, "▱"]
        MAX_QUEUE_SIZE = [int, 5]
        SLEEP_SECS = [int, 10]
        IS_MONGO = [bool, False]

        # Access Restriction
        IS_PRIVATE = [bool, False]
        AUTH_USERS = [list,[123456789]]
        OWNER_ID = [int, 0]

        # Public username url or invite link of private chat
        FORCEJOIN = [str,""]
        FORCEJOIN_ID = [int,-100123465978]

        TRACE_CHANNEL = [int, 0]

try:
    from .tconfig import Commands
except ImportError:
    class Commands:
        START = "/start"
        RENAME = "/rename"
        FILTERS = "/filters"
        SET_THUMB = "/setthumb"
        GET_THUMB = "/getthumb"
        CLR_THUMB = "/clrthumb"
        QUEUE = "/queue"
        MODE = "/mode"
        HELP = "/help"
