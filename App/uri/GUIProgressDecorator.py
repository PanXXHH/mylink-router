import tkinter as tk
import time
import threading
import queue

class GUIProgressDecorator:
    def __init__(self, gui_class, on_close_callback=None):
        self.gui_class = gui_class
        self.on_close_callback = on_close_callback

    def __call__(self, f):
        def wrapped_func(*args, **kwargs):
            stop_event = threading.Event()
            command_queue = queue.Queue()
            gui = self.gui_class(command_queue)
            result = None  # Variable to store the result of the function

            if self.on_close_callback:
                def custom_close():
                    self.on_close_callback(stop_event)
                    command_queue.put('exit')
                gui.set_on_close_callback(custom_close)
            else:
                gui.set_on_close_callback(lambda: stop_event.set())

            def run_task():
                res = f(gui=gui, stop_event=stop_event, *args, **kwargs)
                command_queue.put(('result', res))  # Add a tuple to the queue with the result
                command_queue.put('exit')

            threading.Thread(target=run_task, name="run_task").start()

            try:
                while True:
                    try:
                        command = command_queue.get_nowait()
                        if command == 'exit':
                            # gui.root.quit()
                            gui.root.destroy()
                            break
                        elif command[0] == 'result':
                            result = command[1]  # Get the result from the tuple
                    except queue.Empty:
                        pass
                    gui.root.update_idletasks()
                    gui.root.update()
                    time.sleep(0.05)
            except tk.TclError:
                pass

            return result  # Return the result of the function

        return wrapped_func
