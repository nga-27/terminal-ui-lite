""" Main UI Module """
import time
from enum import Enum
from typing import Union, Callable, List
from threading import Thread
from queue import Queue

from enhanced_input import EnhancedInput
from colorama import just_fix_windows_console


just_fix_windows_console()

DEFAULT_TIMEOUT_FOR_INPUTS = 30.0

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


class TerminalUILite:
    """ Main class of terminal-ui-lite """
    # pylint: disable=too-many-instance-attributes

    def __init__(self, ascii_base_render: Union[List[str], Callable[[], List[str]]]):
        self.__queue = Queue()
        self.__thread = Thread(target=self.__running_view, args=(self.__queue,))
        self.__base_lines = ascii_base_render
        self.__adjustable_lines = []
        self.__adjustable_length = 0
        self.__thread.daemon = True
        self.__thread.start()
        self.__request_callback: Union[Callable, None] = None
        self.__input_timeout = DEFAULT_TIMEOUT_FOR_INPUTS
        self.__input_handler = EnhancedInput().input

    def __running_view(self, queue: Queue):
        """ loads content and runs the terminal view """
        for line in self.__base_lines:
            print(line)
        while True:
            if not queue.empty():
                content = queue.get()
                message_as_input = None
                if isinstance(content, list) and len(content) == 0:
                    self.__adjustable_lines = []
                    for _ in range(self.__adjustable_length):
                        print("\033[A\033[K", end="")
                    self.__adjustable_length = 0

                else:
                    self.__adjustable_lines.append(content)
                    for _ in range(self.__adjustable_length):
                        print("\033[A\033[K", end="")
                    if self.__request_callback:
                        message_as_input = self.__adjustable_lines.pop(-1)
                    self.__adjustable_length = len(self.__adjustable_lines)

                for line in self.__adjustable_lines:
                    print(line)
                if self.__request_callback:
                    data = self.__input_handler(
                        prompt=message_as_input, timeout=self.__input_timeout)
                    self.__request_callback(data)
                    self.__request_callback = None
                    self.__adjustable_length += 1

                    for _ in range(self.__adjustable_length):
                        print("\033[A\033[K", end="")
                    for line in self.__adjustable_lines:
                        print(line)
                    self.__adjustable_length = len(self.__adjustable_lines)
            time.sleep(0.1)

    def add_content(self, content: str, callback_function: Union[Callable, None] = None,
                    input_timeout: Union[int, None] = None,
                    text_color: Union[TextColor, None] = None) -> None:
        """Adds content to the screen terminal

        Args:
            content (str): content to add
            callback_function (Union[Callable, None], optional): callback function for inputs.
                                                        Defaults to None.
            input_timeout (Union[int, None], optional): callback timeout before return None.
                                                        Defaults to None.
            text_color (Union[TextColor, None], optional): color to display content.
                                                        Defaults to None.
        """
        if text_color:
            content = f"{text_color.value}{content}{TextColor.RESET.value}"
        self.__queue.put(content)
        if callback_function:
            self.__request_callback = callback_function
            self.__input_timeout = input_timeout if input_timeout else DEFAULT_TIMEOUT_FOR_INPUTS

    def clear_content(self) -> None:
        """ Clears the non-base content """
        self.__queue.put([])
