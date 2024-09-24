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
        ui_manager.add_content(f"Hello World {i+1}", text_color=colors[i])
        time.sleep(1.5)
    ui_manager.clear_content()
    time.sleep(2)
    ui_manager.add_content("Goodbye")
    time.sleep(2)
    ui_manager.add_content("JK. Fav number? ", test_callback.test_callback)
    test_callback.wait_until_data()
    test_callback.print_data()

if __name__ == "__main__":
    test()
