from itertools import chain
from typing import NamedTuple


test = False


class File(NamedTuple):
    file_name: str
    size: int


class Folder:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.folders = {}
        self.files = []
        self._size = None

    def add_folder(self, folder_name):
        self._size = None
        self.folders[folder_name] = Folder(folder_name, self)

    def add_file(self, file_name, size):
        self._size = None
        self.files.append(File(file_name, size))

    @property
    def size(self):
        if self._size is None:
            self._size = sum(f.size for f in chain(self.files, self.folders.values()))
        return self._size

    def visit_folders(self):
        yield self
        for folder in self.folders.values():
            yield from folder.visit_folders()

    def pprint(self, prefix_len=0):
        prefix = ''.join(' ' for _ in range(prefix_len))
        print(f'{prefix}- {self.name} (dir)')
        for folder in self.folders.values():
            folder.pprint(prefix_len=prefix_len + 2)
        for f in self.files:
            print(f'  {prefix}- {f.file_name} (file, size={f.size})')


def read_data():
    filename = f'puzzle07{"-test" if test else ""}.in'
    with open(filename, 'r') as f:
        file_list = []
        while True:
            try:
                line = next(f).strip().split()
            except StopIteration:
                break
            if line[0] == '$':
                if file_list:
                    yield file_list
                    file_list = []
                yield line[1:]
            else:
                file_list.append(line)
        if file_list:
            yield file_list


def build_filesystem():
    mode = 'cmd'
    cwd = root = Folder('/', parent=None)
    for line in read_data():
        if mode == 'cmd':
            if line[0] == 'cd':
                folder_name = line[1]
                if folder_name == '/':
                    cwd = root
                elif folder_name == '..':
                    cwd = cwd.parent
                else:
                    cwd = cwd.folders[folder_name]
            elif line[0] == 'ls':
                mode = 'ls'
            else:
                raise ValueError('Unexpected command', line)
        else:  # mode == 'ls'
            for item in line:
                if item[0] == 'dir':
                    cwd.add_folder(item[1])
                else:
                    cwd.add_file(item[1], int(item[0]))
            mode = 'cmd'
    return root


def part_1():
    root = build_filesystem()
    return sum(f.size for f in root.visit_folders() if f.size <= 100_000)


def part_2():
    total = 70_000_000
    need_free = 30_000_000
    max_used = total - need_free
    root = build_filesystem()
    used = root.size
    to_free = used - max_used
    choose = min(
        (folder for folder in root.visit_folders() if folder.size >= to_free),
        key=lambda f: f.size
    )
    return choose.size
