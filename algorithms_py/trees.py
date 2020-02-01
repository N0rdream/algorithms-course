import random


class NodeBinary:
    
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.parent = None
        self.l_child = None
        self.r_child = None
        
    def is_l_child(self):
        return self.parent.l_child == self
    
    def is_r_child(self):
        return self.parent.r_child == self
    
    def is_leaf(self):
        return not self.has_l_child and not self.has_r_child()

    def is_root(self):
        return self.parent is None
    
    def has_l_child(self):
        return self.l_child is not None
    
    def has_r_child(self):
        return self.r_child is not None
        
    def insert_node(self, node):
        # если ключ текущего узла меньше чем ключ добавляемого узла
        if self.key < node.key:
            # если у текущего узла есть правый потомок
            if self.has_r_child():
                # добавляем узел в поддерево, где корень - правый потомок текущего узла
                self.r_child.insert_node(node)
            # если у текущего узла нет правого потомка
            else:
                # делаем добавляемый узел правым потомком текущего узла
                self.r_child = node
                # задаем у правого потомка ссылку на родителя, которым является текущий узел
                self.r_child.parent = self
        # если ключ текущего узла больше чем ключ добавляемого узла
        if self.key > node.key:
            # если у текущего узла есть левый потомок
            if self.has_l_child():
                # добавляем узел в поддерево, где корень - левый потомок текущего узла
                self.l_child.insert_node(node)
            # если у текущего узла нет левого потомка
            else:
                # делаем добавляемый узел левым потомком текущего узла
                self.l_child = node
                # задаем у левого потомка ссылку на родителя, которым является текущий узел
                self.l_child.parent = self
                
    def get_node(self, key):
        if self.key == key:
            return self
        elif self.key < key and self.has_r_child():
            return self.r_child.get_node(key)
        elif self.key > key and self.has_l_child():
            return self.l_child.get_node(key)
        
    def remove_node(self):
        # если удаляемый узел является левым потомком своего родителя
        if self.is_l_child():
            # обнуляем у родителя ссылку на левого потомка
            self.parent.l_child = None
        # если правым
        else:
            # обнуляем у родителя ссылку на правого потомка
            self.parent.r_child = None
        # если у удаляемого узла есть левый потомок
        if self.has_l_child():
            # добавляем его в дерево, где корнем является родитель удаляемого узла
            self.parent.insert_node(self.l_child)
        # если у удаляемого узла есть правый потомок
        if self.has_r_child():
            # добавляем его в дерево, где корнем является родитель удаляемого узла
            self.parent.insert_node(self.r_child)
        
    def __iter__(self):
        if self.has_l_child():
            for k, v in self.l_child:
                yield k, v
        yield self.key, self.value
        if self.has_r_child():
            for k, v in self.r_child:
                yield k, v

    # def __len__(self):
    #     if not self.has_l_child() and not self.has_r_child():
    #         return 1
    #     if self.has_l_child() and not self.has_r_child():
    #         return 1 + len(self.l_child)
    #     if not self.has_l_child() and self.has_r_child():
    #         return 1 + len(self.r_child)
    #     return 1 + len(self.l_child) + len(self.r_child)
                
    def rotate(self):
        #
        #       rotate right:                   rotate left:
        #
        #       /           /                 /           /
        #      P           X                 P           X
        #     / \         / \               / \         / \
        #    X  R  --->  L  P      or      L  X  --->  P  R
        #   / \            / \               / \      / \
        #  L  C           C  R              C  R     L  C
        # 
        #  X - node, "new root"; P - node parent, "old root"     
        #
        P = self.parent
        # rotate right
        if self.is_l_child():
            C = self.r_child
            P.l_child = C
            self.r_child = P
        # rotate left
        else:
            C = self.l_child
            P.r_child = C
            self.l_child = P
        self.parent = P.parent
        if P.parent is not None:
            if P.is_l_child():
                P.parent.l_child = self
            elif P.is_r_child():
                P.parent.r_child = self
        P.parent = self
        if C is not None:
            C.parent = P

    def merge(self, node_l, node_r):
        if node_l is None and node_r is None:
            return None
        if node_l is None:
            return node_r
        if node_r is None:
            return node_l
        new_r_child = self.merge(node_l.r_child, node_r)
        if new_r_child is not None:
            new_r_child.parent = node_l
        node_l.r_child = new_r_child
        return node_l

    def _str(self):
        """
        Some visualization magic ispired by MIT 6.006 course materials.
        
        """
        if self.parent is None:
            p = 'None'
        else:
            p = self.parent.key
        label = '(' + str(self.key) + '->' + str(p) + ')'
        if self.l_child is None:
            left_lines, left_pos, left_width = [], 0, 0
        else:
            left_lines, left_pos, left_width = self.l_child._str()
        if self.r_child is None:
            right_lines, right_pos, right_width = [], 0, 0
        else:
            right_lines, right_pos, right_width = self.r_child._str()
        middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
        pos = left_pos + middle // 2
        width = left_pos + middle + right_width - right_pos
        while len(left_lines) < len(right_lines):
            left_lines.append(' ' * left_width)
        while len(right_lines) < len(left_lines):
            right_lines.append(' ' * right_width)
        if (middle - len(label)) % 2 == 1 and self.parent is not None and \
           self is self.parent.l_child and len(label) < middle:
            label += '.'
        label = label.center(middle, '.')
        if label[0] == '.': label = ' ' + label[1:]
        if label[-1] == '.': label = label[:-1] + ' '
        lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                 ' ' * left_pos + '/' + ' ' * (middle-2) +
                 '\\' + ' ' * (right_width - right_pos)] + \
          [left_line + ' ' * (width - left_width - right_width) + right_line
           for left_line, right_line in zip(left_lines, right_lines)]
        return lines, pos, width
    
    def __str__(self):
        return '\n'.join(self._str()[0]) 


class NodeAVL(NodeBinary):
    
    def __init__(self, key, value):
        super().__init__(key, value)
        self.height = 0
        
    def update_height(self):
        if self.has_l_child() and self.has_r_child():
            self.height = max(self.l_child.height, self.r_child.height) + 1
        elif self.has_l_child() and not self.has_r_child():
            self.height = self.l_child.height + 1
        elif not self.has_l_child() and self.has_r_child():
            self.height = self.r_child.height + 1
        else:
            self.height = 0
            
    def get_balance(self):
        if self.has_l_child() and self.has_r_child():
            return self.l_child.height - self.r_child.height
        if self.has_l_child() and not self.has_r_child():
            return self.l_child.height
        if not self.has_l_child() and self.has_r_child():
            return -self.r_child.height
        return 0
    
    def rotate(self):
        old_root = self.parent
        super().rotate()
        old_root.update_height()
        self.update_height()


class NodeRandom(NodeAVL):
    
    def update_heights(self):
        node_parent = self.parent
        while node_parent is not None:
            node_parent.update_height()
            node_parent = node_parent.parent
            
    def insert_root(self, node):
        if self.key < node.key:
            if self.has_r_child():
                self.r_child.insert_root(node)
            else:
                self.r_child = node
                self.r_child.parent = self
        elif self.key > node.key:
            if self.has_l_child():
                self.l_child.insert_root(node)
            else:
                self.l_child = node
                self.l_child.parent = self
        node.rotate()
        
    def merge(self, node_l, node_r):
        node = super().merge(node_l, node_r)
        if node is not None:
            node.update_height()
        return node
        
    def insert_node(self, node):
        if not random.randint(0, self.height):
            self.insert_root(node)
            node.update_heights()
            return
        if self.key < node.key:
            if self.has_r_child():
                self.r_child.insert_node(node)
            else:
                self.r_child = node
                self.r_child.parent = self
        if self.key > node.key:
            if self.has_l_child():
                self.l_child.insert_node(node)
            else:
                self.l_child = node
                self.l_child.parent = self
        node.update_heights()


class NodeSplay(NodeBinary):
        
    def rotate_rr(self):
        # parent and grandparent
        P = self.parent
        G = self.parent.parent
        # Переопределяем потомков (движение от листов к корню)
        G.l_child = P.r_child
        P.r_child = G
        P.l_child = self.r_child
        self.r_child = P
        if not G.is_root():
            if G.is_l_child():
                G.parent.l_child = self
            else:
                G.parent.r_child = self
        # Переопределяем родителей (движение от корня к листам)
        self.parent = G.parent
        P.parent = self
        if P.has_l_child():
            P.l_child.parent = P
        G.parent = P
        if G.has_l_child():
            G.l_child.parent = G
            
    def rotate_ll(self):
        # parent and grandparent
        P = self.parent
        G = self.parent.parent
        # Переопределяем потомков (движение от листов к корню)
        G.r_child = P.l_child
        P.l_child = G
        P.r_child = self.l_child
        self.l_child = P
        if not G.is_root():
            if G.is_l_child():
                G.parent.l_child = self
            else:
                G.parent.r_child = self
        # Переопределяем родителей (движение от корня к листам)
        self.parent = G.parent
        P.parent = self
        if P.has_r_child():
            P.r_child.parent = P
        G.parent = P
        if G.has_r_child():
            G.r_child.parent = G
            
    def rotate_lr(self):
        # parent and grandparent
        P = self.parent
        G = self.parent.parent
        # Переопределяем потомков (движение от листов к корню)
        P.r_child = self.l_child
        G.l_child = self.r_child
        self.l_child = P
        self.r_child = G
        if not G.is_root():
            if G.is_l_child():
                G.parent.l_child = self
            else:
                G.parent.r_child = self
        # Переопределяем родителей (движение от корня к листам)
        self.parent = G.parent
        P.parent = self
        if P.has_r_child():
            P.r_child.parent = P
        G.parent = self
        if G.has_l_child():
            G.l_child.parent = G
            
    def rotate_rl(self):
        # parent and grandparent
        P = self.parent
        G = self.parent.parent
        # Переопределяем потомков (движение от листов к корню)
        P.l_child = self.r_child
        G.r_child = self.l_child
        self.l_child = G
        self.r_child = P
        if not G.is_root():
            if G.is_l_child():
                G.parent.l_child = self
            else:
                G.parent.r_child = self
        # Переопределяем родителей (движение от корня к листам)
        self.parent = G.parent
        P.parent = self
        if P.has_l_child():
            P.l_child.parent = P
        G.parent = self
        if G.has_r_child():
            G.r_child.parent = G
            
    def splay(self):
        if self.is_root():
            return self
        if self.parent.is_root():
            self.rotate()
            return self
        else:
            if self.is_l_child() and self.parent.is_l_child():
                self.rotate_rr()
            elif self.is_l_child() and self.parent.is_r_child():
                self.rotate_rl()
            elif self.is_r_child() and self.parent.is_l_child():
                self.rotate_lr()
            else:
                self.rotate_ll()
        self.splay()


class TreeBinary:
    
    def __init__(self):
        self.root = None
        self.node_type = NodeBinary

    def is_empty(self):
        return self.root is None
        
    def insert(self, key, value):
        node = self.node_type(key, value)
        if self.root is None:
            self.root = node
        else:
            self.root.insert_node(node)
        return node
        
    def has_key(self, key):
        if self.root is not None:
            node = self.root.get_node(key)
            if node is not None:
                return True
        return False

    def get_value(self, key):
        if self.root is not None:
            node = self.root.get_node(key)
            if node is not None:
                return node.value
        raise KeyError
    
    def remove(self, key):
        if self.root is None:
            raise KeyError
        node = self.root.get_node(key)
        if node is None:
            raise KeyError
        if node.parent is not None:
            node.remove_node()
            return node.parent
        else:
            self.set_new_root()
             
    def set_new_root(self):
        if self.root.has_l_child() and not self.root.has_r_child():
            self.root = self.root.l_child
        elif not self.root.has_l_child() and self.root.has_r_child():
            self.root = self.root.r_child
        elif self.root.has_l_child() and self.root.has_r_child():
            R = self.root.r_child
            self.root = self.root.l_child
            self.root.insert_node(R)
        else:
            self.root = None
        if self.root is not None:
            self.root.parent = None
        
    def rotate(self, node):
        node.rotate()
        if node.parent is None:
            self.root = node

    def __iter__(self):
        if self.root is not None:
            for element in self.root:
                yield element
        else:
            return []

    # def __len__(self):
    #     if self.root is not None:
    #         return len(self.root)
    #     else:
    #         return 0


class TreeAVL(TreeBinary):
    
    def __init__(self):
        super().__init__()
        self.node_type = NodeAVL
    
    def insert(self, key, value):
        node = super().insert(key, value)
        self.balance(node)
        
    def remove(self, key):
        node = super().remove(key)
        self.balance(node)
        
    def balance(self, node):
        while node is not None:
            node.update_height()
            node_balance = node.get_balance()
            if node_balance > 1:
                node_l_child_balance = node.l_child.get_balance()
                if node_l_child_balance >= 0:
                    # поворот направо
                    self.rotate(node.l_child)
                else:
                    # поворот налево
                    self.rotate(node.l_child.r_child)
                    # поворот направо
                    self.rotate(node.l_child)
            elif node_balance < -1:
                node_r_child_balance = node.r_child.get_balance()
                if node_r_child_balance <= 0:
                    # поворот налево
                    self.rotate(node.r_child)
                else:
                    # поворот направо
                    self.rotate(node.r_child.l_child)
                    # поворот налево
                    self.rotate(node.r_child)
            node = node.parent


class TreeRandom(TreeBinary):
    
    def __init__(self):
        super().__init__()
        self.node_type = NodeRandom
        
    def insert(self, key, value):
        node = super().insert(key, value)
        if node.parent is None:
            self.root = node
    
    def remove(self, key):
        if self.root is None:
            raise KeyError
        # узел для удаления
        node = self.root.get_node(key)
        if node is None:
            raise KeyError
        # делаем слияние левого и  правого поддеревьев
        node_merge = node.merge(node.l_child, node.r_child)
        # если узел корень, тогда узел слияния - новый корень 
        if node.parent is None:
            self.root = node_merge
            if node_merge is not None:
                self.root.parent = None
        # если узел не корень, тогда
        else:
            # прописываем ссылки на узел слияния у родителя удаляемого узла
            if node.is_l_child():
                node.parent.l_child = node_merge
            if node.is_r_child():
                node.parent.r_child = node_merge
            # устанавливаем родителя узла слияния
            if node_merge is not None:
                node_merge.parent = node.parent
        if node_merge is not None:
            node_merge.update_heights()


class TreeSplay(TreeBinary):
    
    def __init__(self):
        super().__init__()
        self.node_type = NodeSplay 
    
    def has_key(self, key):
        if self.root is None:
            return False
        node = self.root.get_node(key)
        if node is None:
            return False
        node.splay()
        self.root = node
        return True

    def get_value(self, key):
        if self.root is None:
            raise KeyError
        node = self.root.get_node(key)
        if node is None:
            raise KeyError
        node.splay()
        self.root = node
        return node.value
   
    def remove(self, key):
        if self.root is None:
            raise KeyError
        node = self.root.get_node(key)
        if node is None:
            raise KeyError
        node.splay()
        self.root = node.merge(node.l_child, node.r_child)
        if self.root is not None:
            self.root.parent = None