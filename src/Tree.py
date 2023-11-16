class Tree:
    def __init__(self):
        self.treeRoot = {
            "value": -1,
            "prev": None,
            "left": None,
            "right": None
        }
        self.currentRoot = self.treeRoot
        # для поиска наименьших из возможных вершин.
        self.availableNodes = []

    def __del__(self):
        self.__clearLinks()

    def __clearLinks(self):
        pass
