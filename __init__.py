import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from bot.bot_launch import activate
from bot.set_commands import initialise_commands
__all__ = ['activate', 'initialise_commands']



try:
    from bot.bot_launch import activate
    from bot.set_commands import initialise_commands
    __all__ = ['activate', 'initialise_commands']
except:
    __all__=[]
