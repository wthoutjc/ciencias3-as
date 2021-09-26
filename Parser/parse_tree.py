class ParseTree():
    def __init__(self, data):
        self.root = Node(data)

    #PRIVATES

    def __add_recursive(self, node, data):
        if data < node.data:
            if node.left is None:
                node.left = Node(data)
            else:
                self.__add_recursive(node.left, data)
        else:
            if node.right is None:
                node.right = Node(data)
            else:
                self.__add_recursive(node.right, data)

    def __inorder_recursive(self, node):
        if node is not None:
            self.__inorder_recursive(node.left)
            print(node.data, end=', ')
            self.__inorder_recursive(node.right)

    def __preorder_recursive(self, node):
        if node is not None:
            print(node.data, end=', ')
            self.__preorder_recursive(node.left)
            self.__preorder_recursive(node.right)

    def __postorder_recursive(self, node):
        if node is not None:
            self.__preorder_recursive(node.left)
            self.__preorder_recursive(node.right) 
            print(node.data, end=', ')

    def __find(self, node, searching):
        if node is not None:
            return None
        if node.data == searching:
            return node
        if searching < node.data:
            return self.__find(node.left, searching)
        else:
            return self.__find(node.right, searching)

    # PUBLIC

    def add(self, data):
        self.__add_recursive(self.root, data)
    
    def inorder(self):
        self.__inorder_recursive(self.root)

    def preorder(self):
        self.__preorder_recursive(self.root)

    def postorder(self):
        self.__postorder_recursive(self.root)
    
    def find(self, searching):
        return self.__buscar(self.root, searching)

class Node():
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

