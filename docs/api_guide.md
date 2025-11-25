# API Functions

## Initialization

To start the UI, you need to pass in a base string that will serve as the "homepage". These can be elaborate [ASCII ART](https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20) or simple messages saying that the service is running.

```python
ui_manager = TerminalUILite(START_UP_ASCII_STRING)
```

## Base Content Types

### Text Content

The first of 2 base content types is `add_text_content`. This is a base text value that has optional colored text. This function can take a string, number, or other type of value.

```python
ui_manager.add_text_content("this is what will print", text_color: Union[TextColor, None] = TextColor.GREEN)
```

### Input Content

The second of 2 base content types is `add_input_content`. Here, the UI implements a timeout-driven input field (basically the `input` native python function but with an OS-compatible timeout feature so the UI doesn't hang indefinitely waiting input). The default timeout is 30s, but can be whatever is desired.

`add_input_content` also requires a call back function that is given the parameter of `data`, which is the user-input string from the input line. `text_color`, `input_timeout`, and `password_mask` are optional parameters. (`input_timeout` is the aforementioned timeout for the input component.) If the function times out before an input is provided, the callback function data value will return `None`, so check your input validation appropriately.  An example of a callback used in the prescribed way is below:

```python
DEFAULT_DATA_VALUE = "AASDFASDFHLASJFH"

class TestInput:
    # Some weird default because None is a valid timeout data set
    __call_back_data = DEFAULT_DATA_VALUE

    def __call_back_function(data: Any):
        self.__call_back_data = data
        self.ui = TerminalUILite(" STARTING VALUE ")

    def do_something():
        ui_manager.add_input_content("Do you like ice cream? ", self.__call_back_function)
        while self.__call_back_data == DEFAULT_DATA_VALUE:
            time.sleep(0.1)
        data = self.__call_back_data
        # Clear the input call back data
        self.__call_back_data = DEFAULT_DATA_VALUE
```

`password_mask` is `None` by default. When a password-like input (hides the user's input) is needed, add a value for `password_mask` as a "cover up" character. Typical ones are asterisks `'*'` or, for hiding the length of the entry, an empty string `""`. The overall usage of the input is below:

```python
ui_manager.add_input_content(
    "Ask a question? [Y/n] ", callback_function, text_color: Union[Textolor, None] = None, input_timeout: Union[int, None] = None,
    password_mask: Union[str, None] = None)
```

## Content Modification

There are 3 functions that highlight content modification.

### Clear Content

The first is `clear_content`, which does what it sounds like - it clears the _variable_ content. By _variable_, it means that the function will not remove the base "homepage" but will remove everything else. (In future versions, there could be save-able "memory banks" of sets of print outs beyond the base content; i.e. content that might not be as ephemeral as the adjustable content but also not as permanent as the "homepage" content.)

```python
ui_manager.clear_content()
```

### Update Last Text Content

The second of these modification elements is the `update_last_text_content`. In some UI topologies, it's desired to have a message be updated after an operation completes. For example, if the content sent was "Updating data...", it is conceivable that the message after the functional operation was completed could be "Updating data... DONE!". Perhaps this second message could even be green when the first message was white, yellow, or something else. Or, in an error state, it could even be "Updating data... ERROR!" and the text could be red.

In all cases, there is a desire with this UI component to have the ability to update the last line. Yes, you could also do it with the base components if you keep track of UI messages; however, this just simplifies something that could come up more frequently than not.

```python
ui_manager.update_last_text_content("updated message!", text_color: Union[TextColor, None] = TextColor.GREEN)
```

**Note**: any newlines `\n` or return carriages `\r` are removed and ignored with this function, since it _is_ only the last line of the screen. Keep that in mind!

### Clear Print Lines

The third of these modification elements helps adjust the view when rogue prints or warnings appear in the terminal that ruin the overall setup. If these conditions can be tracked programmatically (say, if an exception and warning message occurs, you can track that with the app), then the `clear_print_lines` function can help. It takes only one input, `number_of_lines: int`, and will effectively erase those lines if triggered. 

```python
# Clears 3 lines of prints that happened somehow outside of the developer's control
ui_manager.clear_print_lines(3)
```

## Ellipses (plural of 'ellipsis')

Another fun function of terminal-based UIs is the need for ellipses when running a process. To utilize this, you may run `add_ellipsis_content`. Here, you can optionally specify the rate of ellipses added and the overall duration, within some reason (the combined product of `interval` * `duration` cannot exceed 60. If this product exceeds 60, the `duration` will revert to 60.0 and the `interval` will revert to 1.0.)

When the ellipsis content is completed, it will be removed from the UI. It's recommended to immediately load the next message after this call is made. (For this version, this function is blocking any additional prints from appearing, but they will be queued as usual.)

```python
ui_manager.add_ellipsis_content("message", duration: float = 5.0, interval: float = 1.0, text_color: Union[TextColor, None] = None)
```

In future releases, there will be a secondary function provided that can prematurely stop the ellipsis function. This will require a bit of rework, but it will allow the ellipsis function to serve as a true "loading..." type UI component.

## Miscellaneous

### Centering Offset

Starting with `0.3.3`, users can set the optional field `terminal_centering_offset` that can be determined by finding the center character spot of the terminal. By default, this value will be populated with the center column. This can be updated at any point, either with the instantiation or later (whenever). This allows offsets to the middle offset to be calculated:

```python
# defaults terminal_centering_offset to the middle of the terminal
ui_manager = TerminalUILite(START_UP_ASCII_STRING)

# sets terminal_centering_offset to hardcoded 10
ui_manager = TerminalUILite(START_UP_ASCII_STRING, terminal_centering_offset=10)

# defaults terminal_centering_offset to the middle of the terminal, but then sets it to middle minus 10
ui_manager = TerminalUILite(START_UP_ASCII_STRING)
custom_start_offset = ui_manager.terminal_centering_offset - 10
ui_manager.terminal_centering_offset = custom_start_offset
```

To use this feature, simply call `get_offset()`:

```python
# sets terminal_centering_offset to hardcoded 10
ui_manager = TerminalUILite(START_UP_ASCII_STRING, terminal_centering_offset=10)
# Text will be offset by 10 characters
ui_manager.add_ellipsis_content(f"{ui_manager.get_offset()}Waiting for this to complete", duration=7.0, interval=0.7, text_color=TextColor.YELLOW)
```