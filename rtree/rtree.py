# rtee.py

"""Main Module for the Tree Generator"""

import os
import pathlib

PIPE = "|"
PRE_PIPE = "│   "
ELBOW = "└──"
SPLIT = "├──"
SPACE = "    "

class DirectoryTree:
    def __init__(self, dir_root):
        self._generator = _TreeGenerator(dir_root)

    def generate(self):
        tree = self._generator.build_tree()
        for section in tree:
            print(section)

class _TreeGenerator:
    """Initilizes the class with dir_root
       turning dir_root into a Path object"""
    def __init__(self, dir_root):
        self._dir_root = pathlib.Path(dir_root)
        self._tree = [] # Empyt list that is the start of the diagram

    def build_tree(self):
        """Makes and returns the tree diagram"""
        self._tree_head()
        self._tree_body(self._dir_root)
        return self._tree
    
    def _tree_head(self):
        """Generates the name of the root folder and places
           a PIPE underneath it that then connects to the rest 
           of the diagram"""
        self._tree.append(f"{self._dir_root}{os.sep}")
        self._tree.append(PIPE)

    def _tree_body(self, directory, prefix=""):
        entries = directory.iterdir()
        entries = sorted(entries, key=lambda entry: entry.is_file())
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count -1 else SPLIT
            if entry.is_dir():
                self._add_directory(
                    entry, index, entries_count, prefix, connector
                )
            else:
                self._add_file(entry, prefix, connector)


    def _add_directory(
            self, directory, index, entries_count, prefix, connector
    ):
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")
        if index != entries_count - 1:
            prefix += PRE_PIPE
        else:
            prefix += SPACE
        self._tree_body(
            directory=directory,
            prefix=prefix,
        )
        self._tree.append(prefix.rstrip())


    def _add_file(self, file, prefix, connector):
        self._tree.append(f"{prefix}{connector} {file.name}")