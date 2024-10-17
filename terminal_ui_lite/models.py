""" TerminalUILite Models """
from typing import Union, Callable

DEFAULT_TIMEOUT_FOR_INPUTS = 30.0

class QueueObject:
    """ main queue data object """
    # pylint: disable=too-many-instance-attributes,too-few-public-methods

    def __init__(self, content: Union[str, None] = None, callback: Union[Callable, None] = None, # pylint: disable=too-many-arguments
                 timeout: float = DEFAULT_TIMEOUT_FOR_INPUTS, pw_mask: Union[str, None] = None,
                 only_last: bool = False, ellipsis: bool = False,
                 interval: float = 1.0, duration: float = 5.0):
        self.content = content
        self.callback = callback
        self.timeout = timeout
        self.pw_mask = pw_mask
        self.only_last = only_last
        self.ellipsis = ellipsis
        self.interval = interval
        self.duration = duration
