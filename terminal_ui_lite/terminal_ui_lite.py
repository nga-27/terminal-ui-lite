""" Main UI Module """
import os
import time
from enum import Enum
from typing import Union, Callable, List, Dict, Any
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
        if not isinstance(ascii_base_render, list):
            self.__base_lines = ascii_base_render()
        self.__adjustable_lines = []
        self.__adjustable_length = 0
        self.__thread.daemon = True
        self.__thread.start()
        self.__input_handler = EnhancedInput().input

    def __running_view(self, queue: Queue):
        """ loads content and runs the terminal view """
        # pylint: disable=too-many-branches
        for line in self.__base_lines:
            print(line)
        while True:
            if not queue.empty():
                content: Dict[str, Any] = queue.get()
                message_as_input = None
                if content.get('ellipsis', False):
                    # Doesn't get kept on the list
                    cycles = round(content['duration'] / content['interval'])
                    if cycles > 60:
                        content['interval'] = 1.0
                        content['duration'] = 60.0
                    content["content"] = content["content"].expandtabs(8)
                    for _ in range(cycles):
                        print(content["content"], end="\r")
                        content["content"] += '.'
                        time.sleep(content['interval'])
                    print(" " * (len(content["content"]) + 2), end="\r")
                    continue

                
                terminal_width = os.get_terminal_size()[0]
                for row_i in range(self.__adjustable_length):
                    if row_i < len(self.__adjustable_lines):
                        updated_len = len(self.__adjustable_lines[row_i])
                        while updated_len > terminal_width:
                            print("\033[A\033[K", end="")
                            updated_len -= terminal_width
                    print("\033[A\033[K", end="")

                if content.get('content') is None:
                    self.__adjustable_lines = []
                    self.__adjustable_length = 0
                    continue

                if content['only_last'] and len(self.__adjustable_lines) > 0:
                    self.__adjustable_lines.pop(-1)
                self.__adjustable_lines.append(content["content"])
                # for _ in range(self.__adjustable_length):
                #     print("\033[A\033[K", end="")
                if content["callback"]:
                    message_as_input = self.__adjustable_lines.pop(-1)
                self.__adjustable_length = len(self.__adjustable_lines)

                for line in self.__adjustable_lines:
                    print(line)

                if content['callback']:
                    data = self.__input_handler(
                        prompt=message_as_input, timeout=content['timeout'],
                        password_mask=content['pw_mask'])
                    content["callback"](data)
                    self.__adjustable_length += 1

                    for _ in range(self.__adjustable_length):
                        print("\033[A\033[K", end="")
                    for line in self.__adjustable_lines:
                        print(line)
                    self.__adjustable_length = len(self.__adjustable_lines)
            time.sleep(0.01)

    def add_text_content(self, content: Any, text_color: Union[TextColor, None] = None) -> None:
        """Adds content to the screen terminal

        Args:
            content (str): content to add
            text_color (Union[TextColor, None], optional): color to display content.
                                                        Defaults to None.
        """
        if not isinstance(content, str):
            content = str(content)
        if text_color:
            content = f"{text_color.value}{content}{TextColor.RESET.value}"
        if '\n' in content:
            # Replace any return carriages first, if any
            content = content.replace('\r', '')
            split_content = content.split('\n')
            for spl in split_content:
                queue_able = {
                    "content": spl,
                    "callback": None,
                    "timeout": DEFAULT_TIMEOUT_FOR_INPUTS,
                    "pw_mask": None,
                    "only_last": False
                }
                self.__queue.put(queue_able)

        else:
            queue_able = {
                "content": content,
                "callback": None,
                "timeout": DEFAULT_TIMEOUT_FOR_INPUTS,
                "pw_mask": None,
                "only_last": False
            }
            self.__queue.put(queue_able)

    def add_input_content(self, content: str, callback_function: Callable, # pylint: disable=too-many-arguments
                          input_timeout: Union[int, None] = None,
                          text_color: Union[TextColor, None] = None,
                          password_mask: Union[str, None] = None):
        """Adds content to the screen terminal

        Args:
            content (str): content to add
            callback_function (Union[Callable, None], optional): callback function for inputs.
                                                        Defaults to None.
            input_timeout (Union[int, None], optional): callback timeout before return None.
                                                        Defaults to None.
            text_color (Union[TextColor, None], optional): color to display content.
                                                        Defaults to None.
            password_mask (Union[str, None], optional): Used for a password input. Mask will be the
                                                    hidden password chars. If callback_function is
                                                    None, this is ignored. Default is None.
        """
        if text_color:
            content = f"{text_color.value}{content}{TextColor.RESET.value}"
        if '\n' in content:
            # Replace any return carriages first, if any
            content = content.replace('\r', '')
            split_content = content.split('\n')
            sep_lines = []
            for spl in split_content:
                queue_able = {
                    "content": spl,
                    "callback": None,
                    "timeout": input_timeout if input_timeout else DEFAULT_TIMEOUT_FOR_INPUTS,
                    "pw_mask": None,
                    "only_last": False
                }
                sep_lines.append(queue_able.copy())
            sep_lines[-1]["callback"] = callback_function
            if password_mask is not None:
                sep_lines[-1]["pw_mask"] = password_mask
            for line in sep_lines:
                self.__queue.put(line)

        else:
            queue_able = {
                "content": content,
                "callback": callback_function,
                "timeout": input_timeout if input_timeout else DEFAULT_TIMEOUT_FOR_INPUTS,
                "pw_mask": password_mask,
                "only_last": False
            }
            self.__queue.put(queue_able)

    def update_last_text_content(self, content: str,
                                 text_color: Union[TextColor, None] = None) -> None:
        """update the last line of content
        Rejects any new lines or carriage returns

        Args:
            content (str): string to display
            text_color (Union[TextColor, None], optional): optional color. Defaults to None.
        """
        if text_color:
            content = f"{text_color.value}{content}{TextColor.RESET.value}"
        # Rejects new lines
        content = content.replace("\r", "").replace("\n", " ")
        queue_able = {
            "content": content,
            "callback": None,
            "timeout": DEFAULT_TIMEOUT_FOR_INPUTS,
            "pw_mask": None,
            "only_last": True
        }
        self.__queue.put(queue_able)

    def add_ellipsis_content(self, content: str, duration: float = 5.0, interval: float = 1.0,
                             text_color: Union[TextColor, None] = None):
        """Add content that will be like a "loading" screen with additional ellipses

        Args:
            content (str): message that will have the ellipsis appended to
            duration (float, optional): duration (in s) of blocking ellipsis view. Defaults to 5.0.
            interval (float, optional): interval (in s) of printed periods. Defaults to 1.0.
            text_color (Union[TextColor, None], optional): text color. Defaults to None.
        """
        if not len(content) < 3 or '...' == content[-3:]:
            content += "..."
        if text_color:
            content = f"{text_color.value}{content}{TextColor.RESET.value}"
        # Rejects new lines
        content = content.replace("\r", "").replace("\n", " ")
        queue_able = {
            "content": content,
            "callback": None,
            "timeout": DEFAULT_TIMEOUT_FOR_INPUTS,
            "pw_mask": None,
            "only_last": False,
            "ellipsis": True,
            "interval": interval,
            "duration": duration
        }
        self.__queue.put(queue_able)

    def clear_content(self) -> None:
        """ Clears the non-base content """
        self.__queue.put({})

    def clear_print_lines(self, number_of_lines: int) -> None:
        """ Erases 'number_of_lines' from the screen, useful when prints crowd terminal view """
        if number_of_lines < 0:
            number_of_lines = 0
        for _ in range(number_of_lines):
            print("\033[A\033[K", end="")
