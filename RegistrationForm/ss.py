import math
import threading
import time
import tkinter.ttk
import uuid
from tkinter.constants import EW, NSEW, SE


class Application(tkinter.ttk.Frame):
    FPS = 10  # frames per second used to update the graph
    MARGINS = 10, 10, 10, 10  # internal spacing around the graph

    @classmethod
    def main(cls):
        tkinter.NoDefaultRoot()
        root = tkinter.Tk()
        root.title('Tkinter Graphing')
        # noinspection SpellCheckingInspection
        root.minsize(640, 480)  # VGA (NTSC)
        cls(root).grid(sticky=NSEW)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.mainloop()

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.display = tkinter.Canvas(self, background='white')
        self.display.bind('<Configure>', self.draw)
        self.start = StatefulButton(self, 'Start Graphing', self.start_graph)
        self.grip = tkinter.ttk.Sizegrip(self)
        self.grid_widgets(padx=5, pady=5)
        self.data_source = DataSource()
        self.after_idle(self.update_graph, round(1000 / self.FPS))
        self.run_graph = None

    def grid_widgets(self, **kw):
        self.display.grid(row=0, column=0, columnspan=2, sticky=NSEW, **kw)
        self.start.grid(row=1, column=0, sticky=EW, **kw)
        self.grip.grid(row=1, column=1, sticky=SE)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def start_graph(self):
        self.run_graph = True
        threading.Thread(target=self.__simulate, daemon=True).start()
        return 'Stop Graphing', self.stop_graph

    def stop_graph(self):
        self.run_graph = False
        return 'Clear Graph', self.clear_graph

    def clear_graph(self):
        self.data_source.clear()
        self.reset_display()
        return 'Start Graphing', self.start_graph

    # def __simulate(self):
    #     # simulate changing populations
    #     for population in itertools.count():
    #         if not self.run_graph:
    #             break
    #         self.data_source.append(population, get_max_age(population, 200))

    # def __simulate(self):
    #     # simulate changing ages
    #     for age in itertools.count(1):
    #         if not self.run_graph:
    #             break
    #         self.data_source.append(age, get_max_age(250_000_000, age))

    def __simulate(self):
        # draw a sine curve
        for x in range(800):
            time.sleep(0.01)
            if not self.run_graph:
                break
            self.data_source.append(x, math.sin(x * math.pi / 400))

    def update_graph(self, rate, previous_version=None):
        if previous_version is None:
            self.reset_display()
        current_version = self.data_source.version
        if current_version != previous_version:
            data_source = self.data_source.copy()
            self.draw(data_source)
        self.after(rate, self.update_graph, rate, current_version)

    def reset_display(self):
        self.display.delete('data')
        self.display.create_line((0, 0, 0, 0), tag='data', fill='black')

    def draw(self, data_source):
        if not isinstance(data_source, DataSource):
            data_source = self.data_source.copy()
        if data_source:
            self.display.coords('data', *data_source.frame(
                self.MARGINS,
                self.display.winfo_width(),
                self.display.winfo_height(),
                True
            ))


class StatefulButton(tkinter.ttk.Button):
    def __init__(self, master, text, command, **kw):
        kw.update(text=text, command=self.__do_command)
        super().__init__(master, **kw)
        self.__command = command

    def __do_command(self):
        self['text'], self.__command = self.__command()


def new(obj):
    kind = type(obj)
    return kind.__new__(kind)


def interpolate(x, y, z):
    return x * (1 - z) + y * z


def interpolate_array(array, z):
    if z <= 0:
        return array[0]
    if z >= 1:
        return array[-1]
    share = 1 / (len(array) - 1)
    index = int(z / share)
    x, y = array[index:index + 2]
    return interpolate(x, y, z % share / share)


def sample(array, count):
    scale = count - 1
    return tuple(interpolate_array(array, z / scale) for z in range(count))


class DataSource:
    EMPTY = uuid.uuid4()

    def __init__(self):
        self.__x = []
        self.__y = []
        self.__version = self.EMPTY
        self.__mutex = threading.Lock()

    @property
    def version(self):
        return self.__version

    def copy(self):
        instance = new(self)
        with self.__mutex:
            instance.__x = self.__x.copy()
            instance.__y = self.__y.copy()
            instance.__version = self.__version
        instance.__mutex = threading.Lock()
        return instance

    def __bool__(self):
        return bool(self.__x or self.__y)

    def frame(self, margins, width, height, auto_sample=False, timing=False):
        if timing:
            start = time.perf_counter()
        x1, y1, x2, y2 = margins
        drawing_width = width - x1 - x2
        drawing_height = height - y1 - y2
        with self.__mutex:
            x_tuple = tuple(self.__x)
            y_tuple = tuple(self.__y)
        if auto_sample and len(x_tuple) > drawing_width:
            x_tuple = sample(x_tuple, drawing_width)
            y_tuple = sample(y_tuple, drawing_width)
        max_y = max(y_tuple)
        x_scaling_factor = max(x_tuple) - min(x_tuple)
        y_scaling_factor = max_y - min(y_tuple)
        coords = tuple(
            coord
            for x, y in zip(x_tuple, y_tuple)
            for coord in (
                round(x1 + drawing_width * x / x_scaling_factor),
                round(y1 + drawing_height * (max_y - y) / y_scaling_factor)))
        if timing:
            # noinspection PyUnboundLocalVariable
            print(f'len = {len(coords) >> 1}; '
                  f'sec = {time.perf_counter() - start:.6f}')
        return coords

    def append(self, x, y):
        with self.__mutex:
            self.__x.append(x)
            self.__y.append(y)
            self.__version = uuid.uuid4()

    def clear(self):
        with self.__mutex:
            self.__x.clear()
            self.__y.clear()
            self.__version = self.EMPTY

    def extend(self, iterable):
        with self.__mutex:
            for x, y in iterable:
                self.__x.append(x)
                self.__y.append(y)
            self.__version = uuid.uuid4()


if __name__ == '__main__':
    Application.main()