"""
1. add a new element (lst.add(3), cons(lst, 3), extend(lst, 3));
2. remove an element (lst.remove(3), remove(lst, 3));
3. size (lst.size(), size(lst));
4. conversion from and to python lists (lst.to_list(), lst.from_list([12, 99, 37]), from_list([12, 99, 37]));
5. find element by specific predicate (lst.find(is_even_), );
6. filter data structure by specific predicate (lst.filter(is_even));
7. map structure by specific function (lst.map(increment));
8. reduce – process structure elements to build a return value by specific functions (lst.reduce(sum));
9. data structure should be a monoid and implement mempty and mconcat functions or methods;
10. iterator:
for the mutable version in Python style [12, Chapter 7. Classes & Iterators];
for the immutable version by closure [14], see example ahead.
"""

def sum(a,b):
    return a+b

def f(value):
    if type(value) == int:
        value = value * 2
    return value

class binary_tree_node(object):
    def __init__(self,value=-1,left=None,right=None):
        """init node class"""
        self.value = value
        self.left = left
        self.right = right

    def get_value(self):
        """return node.element"""
        return self.value

class binary_tree(object):
    def __init__(self,root=None):
        self.root = root

    def add_node_in_order(self,value):
        new_node = binary_tree_node(value)
        if self.root is None:
            self.root = new_node
        else:
            node_queue = list()
            node_queue.append(self.root)
            while len(node_queue):
                q_node = node_queue.pop(0)
                if q_node.left is None:
                    q_node.left = new_node
                    break
                elif q_node.right is None:
                    q_node.right = new_node
                    break
                else:
                    node_queue.append(q_node.left)
                    node_queue.append(q_node.right)

    def get_parent(self, value):
        if self.root.value == value:
            return None
        tmp = [self.root]
        while tmp:
            pop_node = tmp.pop(0)
            if pop_node.left and pop_node.left.value == value:
                return pop_node
            if pop_node.right and pop_node.right.value == value:
                return pop_node
            if pop_node.left is not None:
                tmp.append(pop_node.left)
            if pop_node.right is not None:
                tmp.append(pop_node.right)
        return None

    def remove(self, value):
        if self.root is None:
            return False
        parent = self.get_parent(value)
        if parent:
            del_node = parent.left if parent.left.value == value else parent.right  # 待删除节点
            if del_node.left is None:
                if parent.left.value == value:
                    parent.left = del_node.right
                else:
                    parent.right = del_node.right
                #del del_node
                return True
            elif del_node.right is None:
                if parent.left.value == value:
                    parent.left = del_node.left
                else:
                    parent.right = del_node.left
                #del del_node
                return True
            else:  # 左右子树都不为空
                tmp_pre = del_node
                tmp_next = del_node.right
                if tmp_next.left is None:
                    # 替代
                    tmp_pre.right = tmp_next.right
                    tmp_next.left = del_node.left
                    tmp_next.right = del_node.right
                else:
                    while tmp_next.left:  # 让tmp指向右子树的最后一个叶子
                        tmp_pre = tmp_next
                        tmp_next = tmp_next.left
                    # 替代
                    tmp_pre.left = tmp_next.right
                    tmp_next.left = del_node.left
                    tmp_next.right = del_node.right
                if parent.left.value == value:
                    parent.left = tmp_next
                else:
                    parent.right = tmp_next
                #del del_node
                return True
        else:
            return False

    def preorder2list(self):
        """method of traversing BiTree in pre-order"""
        if self.root is None:
            return None
        else:
            node_stack = list()
            output_list = list()
            node = self.root
            while node is not None or len(node_stack):
                if node is None:
                    node = node_stack.pop().right
                    continue
                while node.left is not None:
                    node_stack.append(node)
                    output_list.append(node.get_value())
                    node = node.left
                output_list.append(node.get_value())
                node = node.right
        return output_list

    def inorder2list(self):
        """method of traversing BiTree in pre-order"""
        if self.root is None:
            return None
        else:
            node_stack = list()
            output_list = list()
            node = self.root
            while node is not None or len(node_stack):
                if node is None:
                    node = node_stack.pop()
                    output_list.append(node.get_value())
                    node = node.right
                    continue
                while node.left is not None:
                    node_stack.append(node)
                    node = node.left
                output_list.append(node.get_value())
                node = node.right
        return output_list

    def postorder2list(self):
        """method of traversing BiTree in pre-order"""
        if self.root is None:
            return None
        else:
            node_stack = list()
            output_list = list()
            node = self.root
            while node is not None or len(node_stack):
                if node is None:
                    node = node_stack.pop().left
                    continue
                while node.right is not None:
                    node_stack.append(node)
                    output_list.append(node.get_value())
                    node = node.right
                output_list.append(node.get_value())
                node = node.left
        return output_list[::-1]

    def size(self):
        if self.root is None:
            return 0
        else:
            lst = self.preorder2list()
            return len(lst)

    def lst2bt(self,lst):
        final_tree = binary_tree()
        for i in range(len(lst)):
            final_tree.add_node_in_order(lst[i])
        return final_tree

    def pre_order_index(self,value):
        pre_lst = self.preorder2list()
        return pre_lst.index(value)

    def in_order_index(self,value):
        in_lst = self.inorder2list()
        return in_lst.index(value)

    def post_order_index(self,value):
        post_lst = self.postorder2list()
        return post_lst.index(value)

    def tree_filter(self):
        lst = self.preorder2list()
        f = []
        for i in range(len(lst)):
            if type(lst[i]) == int:
                f.append(lst[i])
        return f

    def tree_map(self, f):
        listmap = self.preorder2list()
        for i in range(len(listmap)):
            listmap[i] = f(listmap[i])
        return listmap

    def reduce(self,sum):
        result = 0
        if self.root is None:
            return None
        else:
            node_stack = list()
            node = self.root
            while node is not None or len(node_stack):
                if node is None:
                    node = node_stack.pop().right
                    continue
                while node.left is not None:
                    node_stack.append(node)
                    result = sum(result,node.get_value())
                    node = node.left
                result = sum(result, node.get_value())
                node = node.right
        return result

    def tree_mconcat(self,t1,t2):
        if not t1:
            return t2
        if not t2:
            return t1
        root = binary_tree_node(t1.value + t2.value)
        root.left = self.tree_mconcat(t1.left, t2.left)
        root.right = self.tree_mconcat(t1.right, t2.right)
        return root

    def isEqual(self,tree):
        root1 = self.root
        root2 = tree.root
        if root1 is None and root2 is None:
            return True
        if root1 is None and root2 is not None:
            return False
        if root1 is not None and root2 is None:
            return False
        if root1.value == root2.value:
            return binary_tree(root1.left).isEqual(binary_tree(root2.left)) and binary_tree(root1.right).isEqual(binary_tree(root2.right))
        else:
            return False

    def __iter__(self):
        return binary_tree(self.root)















