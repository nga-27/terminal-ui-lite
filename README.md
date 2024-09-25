# terminal-ui-lite
A light-weight way to have a terminal as a basic UI for servers and non-graphical UIs.

<img src="static/jungle_for_terminal.jpeg" alt="jungle out there" width=400 />

---

# Installation

```sh
pip install terminal_ui_lite @ git+ssh://git@github.com/nga-27/terminal-ui-lite.git@v0.2.0
```

---

# Usage

An example script is below. Note that `TestCallBack` is just to demonstrate the callback features of the input prompts. This can be run directly with `test.py`.

```python
from terminal_ui_lite import TerminalUILite, TextColor

class TestCallback:
    def __init__(self):
        self.data = None

    def test_callback(self, data):
        self.data = data

    def wait_until_data(self):
        while not self.data:
            time.sleep(0.1)
        return self.data
    
    def clear_data(self):
        self.data = None
    
    def print_data(self):
        print(self.data)

START_UP = ["""
    HI THERE!!!! THIS IS MY APP
"""]

# THE ACTUAL CODE
def test():
    # START_UP represents the "baseline" view that should always be displayed. (ASCII art is recommended)
    ui_manager = TerminalUILite(START_UP)
    test_callback = TestCallback()
    time.sleep(2)
    colors = [TextColor.RED, TextColor.GREEN, TextColor.BLUE]
    # Add colors of repeated text
    for i in range(3):
        ui_manager.add_text_content(f"Hello World {i+1}", text_color=colors[i])
        time.sleep(1.5)
    time.sleep(3)
    ui_manager.clear_content()
    time.sleep(2)

    # Speed test the queue - it should print almost instantaneously, but with a several 100ms delay
    ui_manager.add_text_content("bah")
    ui_manager.add_text_content("bye")
    ui_manager.add_text_content("x")
    ui_manager.add_input_content("huh? ", test_callback.test_callback)
    test_callback.wait_until_data()
    test_callback.clear_data()

    # Over write the last line, as in like a status update
    ui_manager.add_text_content("checking...")
    time.sleep(1)
    ui_manager.update_last_text_content("checking... Done!", TextColor.GREEN)
    time.sleep(1)
    # for update_last_text_content, newlines and carriage returns are ignored
    ui_manager.update_last_text_content("checking...\n ERROR!", TextColor.RED)
    time.sleep(2)
    ui_manager.clear_content()
    time.sleep(2)

    # for input and text content, \r is removed and \n is added as correct functionality
    ui_manager.add_input_content("hello\r\nthere\nObi-Wan ", callback_function=test_callback.test_callback,
                                 password_mask="*")
    test_callback.wait_until_data()
    test_callback.print_data()


if __name__ == "__main__":
    test()
```