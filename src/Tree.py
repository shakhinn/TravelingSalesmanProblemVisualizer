class Tree:
    def __init__(self, matrix):
        self.treeRoot = {
            "path": [],
            "value": -1,
            "matrix": matrix,
            "city_rows": [i for i in range(len(matrix))],
            "city_cols": [i for i in range(len(matrix))],
            "cycles": {},
            "prev": None,
            "left": None,
            "right": None,
        }
        self.currentRoot = self.treeRoot
        # для поиска наименьших из возможных вершин.
        self.availableNodes = []

    def __del__(self):
        self.__clearLinks(self.treeRoot)
        self.treeRoot = None
        self.currentRoot = None

    def __clearLinks(self, node):
        if node is None:
            return
        self.__clearLinks(node["left"])
        node["left"] = None
        self.__clearLinks(node["right"])
        node["right"] = None
        node["prev"] = None
