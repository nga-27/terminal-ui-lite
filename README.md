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

---

# API Functions

## Initialization

To start the UI, you need to pass in a base string that will serve as the "homepage". These can be elaborate [ASCII ART](https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20) or simple messages saying that the service is running.

```python
ui_manager = TerminalUILite(START_UP_ASCII_STRING)
```

## Base Content Types

The first of 2 base content types is `add_text_content`. This is a base text value that has optional colored text.

```python
ui_manager.add_text_content("this is what will print", text_color: Union[TextColor, None] = TextColor.GREEN)
```

The second of 2 base content types is `add_input_content`. Here, the UI implements a timeout-driven input field (basically the `input` native python function but with an OS-compatible timeout feature so the UI doesn't hang indefinitely waiting input). The default timeout is 30s, but can be whatever is desired.

`add_input_content` also requires a call back function that is given the parameter of `data`, which is the user-input string from the input line. `text_color`, `input_timeout`, and `password_mask` are optional parameters. (`input_timeout` is the aforementioned timeout for the input component.)

`password_mask` is `None` by default. When a password-like input (hides the user's input) is needed, add a value for `password_mask` as a "cover up" character. Typical ones are asterisks `'*'` or, for hiding the length of the entry, an empty string `""`.

```python
ui_manager.add_input_content(
    "Ask a question? [Y/n] ", callback_function, text_color: Union[Textolor, None] = None, input_timeout: Union[int, None] = None,
    password_mask: Union[str, None] = None)
```

## Content Modification

There are 2 functions that highlight content modification. The first is `clear_content`, which does what it sounds like - it clears the _variable_ content. By _variable_, it means that the function will not remove the base "homepage" but will remove everything else. (In future versions, there could be save-able "memory banks" of sets of print outs beyond the base content; i.e. content that might not be as ephemeral as the adjustable content but also not as permanent as the "homepage" content.)

```python
ui_manager.clear_content()
```

The second of these modification elements is the `update_last_text_content`. In some UI topologies, it's desired to have a message be updated after an operation completes. For example, if the content sent was "Updating data...", it is conceivable that the message after the functional operation was completed could be "Updating data... DONE!". Perhaps this second message could even be green when the first message was white, yellow, or something else. Or, in an error state, it could even be "Updating data... ERROR!" and the text could be red.

In all cases, there is a desire with this UI component to have the ability to update the last line. Yes, you could also do it with the base components if you keep track of UI messages; however, this just simplifies something that could come up more frequently than not.

```python
ui_manager.update_last_text_content("updated message!", text_color: Union[TextColor, None] = TextColor.GREEN)
```

**Note**: any newlines `\n` or return carriages `\r` are removed and ignored with this function, since it _is_ only the last line of the screen. Keep that in mind!

## Ellipses (plural of 'ellipsis')

Another fun function of terminal-based UIs is the need for ellipses when running a process. To utilize this, you may run `add_ellipsis_content`. Here, you can optionally specify the rate of ellipses added and the overall duration, within some reason (the combined product of `interval` * `duration` cannot exceed 60. If this product exceeds 60, the `duration` will revert to 60.0 and the `interval` will revert to 1.0.)

When the ellipsis content is completed, it will be removed from the UI. It's recommended to immediately load the next message after this call is made. (For this version, this function is blocking any additional prints from appearing, but they will be queued as usual.)

```python
ui_manager.add_ellipsis_content("message", duration: float = 5.0, interval: float = 1.0, text_color: Union[TextColor, None] = None)
```

In future releases, there will be a secondary function provided that can prematurely stop the ellipsis function. This will require a bit of rework, but it will allow the ellipsis function to serve as a true "loading..." type UI component.
