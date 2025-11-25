import time
import os
from typing import List

from terminal_ui_lite import TerminalUILite, TextColor

class TestCallback:
    def __init__(self):
        self.data = "FASDFASDFASDFASDAF"

    def test_callback(self, data):
        self.data = data

    def wait_until_data(self):
        while self.data == "FASDFASDFASDFASDAF":
            time.sleep(0.1)
        return self.data
    
    def clear_data(self):
        self.data = "FASDFASDFASDFASDAF"
    
    def print_data(self) -> str:
        # print(self.data)
        return self.data

START_UP = """
    HI THERE!!!! THIS IS MY APP
"""

def start_up_text() -> List[str]:
    lines = []
    lines.append(" ")
    lines.append(START_UP)
    lines.append(" ")
    lines.append(" mysterious other thing ")
    lines.append(" ")
    return lines

def test():
    ui_manager = TerminalUILite(start_up_text(), terminal_centering_offset=15)
    test_callback = TestCallback()
    time.sleep(2)
    colors = [TextColor.RED, TextColor.GREEN, TextColor.BLUE]
    ui_manager.add_text_content(8)
    ui_manager.add_text_content({"hello": "there"})
    garbage = {f"key{x}": f"value{x}" for x in range(15)}
    ui_manager.add_text_content(garbage)
    ui_manager.add_text_content(len(garbage))
    ui_manager.add_text_content(len(str(garbage)))
    for i in range(3):
        ui_manager.add_text_content(f"Hello World {i+1}", text_color=colors[i])
        time.sleep(1.5)
    time.sleep(3)
    ui_manager.clear_content()
    time.sleep(2)
    term_width = os.get_terminal_size()[0]
    ui_manager.add_text_content("**" * (2 * term_width))
    time.sleep(2)
    ui_manager.clear_content()
    time.sleep(3)
    ui_manager.add_text_content("bah")
    ui_manager.add_text_content("bye")
    ui_manager.add_text_content("x")
    ui_manager.add_input_content("huh? ", test_callback.test_callback, input_timeout=15)
    test_callback.wait_until_data()
    test_callback.clear_data()
    ui_manager.add_text_content("checking....")
    time.sleep(1)
    ui_manager.update_last_text_content("checking.... OK!", TextColor.GREEN)
    time.sleep(1)
    ui_manager.update_last_text_content("checking....\n ERROR!", TextColor.RED)
    time.sleep(2)
    ui_manager.clear_content()
    time.sleep(2)
    ui_manager.add_input_content("hello\r\nthere\nObi-Wan ", callback_function=test_callback.test_callback,
                                 password_mask="*")
    test_callback.wait_until_data()
    ui_manager.add_text_content(test_callback.print_data())
    time.sleep(2)
    ui_manager.clear_content()
    time.sleep(1)
    ui_manager.add_ellipsis_content(f"{ui_manager.get_offset()}Waiting for this to complete", duration=7.0, interval=0.7, text_color=TextColor.YELLOW)
    ui_manager.add_text_content("Immediately after!", text_color=TextColor.GREEN)
    time.sleep(12)
    print(f"Offset is: {ui_manager.terminal_centering_offset} (should be 15)")



if __name__ == "__main__":
    test()
