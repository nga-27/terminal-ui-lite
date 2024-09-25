import time

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

def test():
    ui_manager = TerminalUILite(START_UP)
    test_callback = TestCallback()
    time.sleep(2)
    colors = [TextColor.RED, TextColor.GREEN, TextColor.BLUE]
    for i in range(3):
        ui_manager.add_text_content(f"Hello World {i+1}", text_color=colors[i])
        time.sleep(1.5)
    time.sleep(3)
    ui_manager.clear_content()
    time.sleep(2)
    ui_manager.add_text_content("bah")
    ui_manager.add_text_content("bye")
    ui_manager.add_text_content("x")
    ui_manager.add_input_content("huh? ", test_callback.test_callback)
    test_callback.wait_until_data()
    test_callback.clear_data()
    time.sleep(2)
    ui_manager.clear_content()
    time.sleep(2)
    ui_manager.add_input_content("hello\r\nthere\nObi-Wan ", callback_function=test_callback.test_callback,
                                 password_mask="*")
    test_callback.wait_until_data()
    test_callback.print_data()

if __name__ == "__main__":
    test()
