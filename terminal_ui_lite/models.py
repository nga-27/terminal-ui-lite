""" TerminalUILite Models """
from typing import Union, Callable
from enum import Enum


DEFAULT_TIMEOUT_FOR_INPUTS = 30.0
MAX_TIME_FOR_CONTROLLED_ELLIPSE = 10 * 60  # 10 minutes


class TextColor(Enum):
    """ Color options that are supported """
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[39m"


class QueueObject:
    """ main queue data object """
    # pylint: disable=too-many-instance-attributes,too-few-public-methods

    def __init__(self, content: Union[str, None] = None, callback: Union[Callable, None] = None, # pylint: disable=too-many-arguments
                 timeout: float = DEFAULT_TIMEOUT_FOR_INPUTS, pw_mask: Union[str, None] = None,
                 only_last: bool = False, ellipsis: bool = False,
                 interval: float = 1.0, duration: float = 5.0,
                 start_controlled_ellipse: bool = False, text_color: Union[TextColor, None] = None,
                 end_controlled_message: str = "... done."):
        self.content = content
        self.callback = callback
        self.timeout = timeout
        self.pw_mask = pw_mask
        self.only_last = only_last
        self.ellipsis = ellipsis
        self.interval = interval
        self.duration = duration
        self.start_controlled_ellipse = start_controlled_ellipse
        self.text_color = TextColor.RESET
        if text_color:
            self.text_color = text_color
        self.end_controlled_message = end_controlled_message
