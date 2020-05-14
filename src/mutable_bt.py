"""
- Add .gitignore.

- You should insert fig into markdown documents (`![Alt text](/path/to/img.jpg)`).

- Why you prefer manual stack usage over recursive functions?

- You should translate commentaries into English.

- Add property-based tests for from_list and to_list, all monoid properties.

- For writing more readable code, you should use the naming style: https://www.python.org/dev/peps/pep-0008/

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


def mul(value):
    if type(value) == int:
        value = value * 2
    return value


class BinaryTreeNode(object):
    def __init__(self, value=-1, left=None, right=None):
        """node constructor"""
        self.value = value
        self.left = left
        self.right = right

    def get_value(self):
        """return node value"""
        return self.value


class BinaryTree(object):
    def __init__(self, root=None):
        self.root = root
        self.level_queue = []
        self.cur = 0

    def add_node_in_order(self, value):
        """add new node in order"""
        new_node = BinaryTreeNode(value)
        if self.root is None:
            self.root = new_node
        else:
            node_queue = list()
            node_queue.append(self.root)
            while len(node_queue):
                cur = node_queue.pop(0)
                if cur.left is None:
                    cur.left = new_node
                    break
                elif cur.right is None:
                    cur.right = new_node
                    break
                else:
                    node_queue.append(cur.left)
                    node_queue.append(cur.right)

    def get_parent(self, value):
        """return node's parent"""
        if self.root.value == value:
            return None
        node_queue = list()
        node_queue.append(self.root)
        while len(node_queue):
            cur = node_queue.pop(0)
            if cur.left and cur.left.value == value:
                return cur
            if cur.right and cur.right.value == value:
                return cur
            if cur.left is not None:
                node_queue.append(cur.left)
            if cur.right is not None:
                node_queue.append(cur.right)
        return None

    def remove(self, value):
        """remove node whose .value is value"""
        if self.root is None:
            return False
        if self.root.value == value:
            self.root = None
            return True
        parent = self.get_parent(value)
        if parent:
            if parent.left.value == value:
                del_node = parent.left
            else:
                del_node = parent.right
            if del_node.left is None:
                if parent.left.value == value:
                    parent.left = del_node.right
                else:
                    parent.right = del_node.right
                return True
            elif del_node.right is None:
                if parent.left.value == value:
                    parent.left = del_node.left
                else:
                    parent.right = del_node.left
                return True
            else:
                tmp_pre = del_node
                tmp_next = del_node.right
                if tmp_next.left is None:
                    tmp_pre.right = tmp_next.right
                    tmp_next.left = del_node.left
                    tmp_next.right = del_node.right
                else:
                    while tmp_next.left:
                        tmp_pre = tmp_next
                        tmp_next = tmp_next.left
                    tmp_pre.left = tmp_next.right
                    tmp_next.left = del_node.left
                    tmp_next.right = del_node.right
                if parent.left.value == value:
                    parent.left = tmp_next
                else:
                    parent.right = tmp_next
                return True
        else:
            return False

    def to_list_pre_order(self):
        """return list in pre-order"""
        if self.root is None:
            return []
        else:
            left_lst = BinaryTree(self.root.left).to_list_pre_order()
            right_lst = BinaryTree(self.root.right).to_list_pre_order()
            if left_lst is None and right_lst is None:
                return [self.root.value]
            if left_lst is None:
                return [self.root.value] + right_lst
            if right_lst is None:
                return [self.root.value] + left_lst
            return [self.root.value] + left_lst + right_lst            

    def to_list_in_order(self):
        """return list in in-order"""
        if self.root is None:
            return []
        else:
            left_lst = BinaryTree(self.root.left).to_list_in_order()
            right_lst = BinaryTree(self.root.right).to_list_in_order()
            if left_lst is None and right_lst is None:
                return [self.root.value]
            if left_lst is None:
                return [self.root.value] + right_lst
            if right_lst is None:
                return left_lst + [self.root.value]
            return left_lst + [self.root.value] + right_lst

    def to_list_post_order(self):
        """return list in post-order"""
        if self.root is None:
            return []
        else:
            left_lst = BinaryTree(self.root.left).to_list_post_order()
            right_lst = BinaryTree(self.root.right).to_list_post_order()
            if left_lst is None and right_lst is None:
                return [self.root.value]
            if left_lst is None:
                return right_lst + [self.root.value]
            if right_lst is None:
                return left_lst + [self.root.value]
            return left_lst + right_lst + [self.root.value]

    def get_depth(self):
        """return the depth of the binary tree"""
        if self.root is None:
            return 0
        depth = 1
        left_depth = BinaryTree(self.root.left).get_depth()
        right_depth = BinaryTree(self.root.right).get_depth()
        if left_depth == 0 and right_depth == 0:
            return depth
        if left_depth > right_depth:
            return depth+left_depth
        else:
            return depth+right_depth

    def to_list_level_order(self):
        """return list in level-order"""
        if self.root is None:
            return []
        lst = list()
        node_queue = list()
        node_queue.append(self.root)
        while len(node_queue):
            cur = node_queue.pop(0)
            lst.append(cur.value)
            if cur.left is not None:
                node_queue.append(cur.left)
            if cur.right is not None:
                node_queue.append(cur.right)
        return lst

    def size(self):
        """return the number of nodes in binary tree"""
        if self.root is None:
            return 0
        left_size = BinaryTree(self.root.left).size()
        right_size = BinaryTree(self.root.right).size()
        if left_size == 0 and right_size == 0:
            return 1
        elif left_size == 0:
            return 1+right_size
        elif right_size == 0:
            return 1+left_size
        else:
            return 1+left_size+right_size

    def from_list(self, lst):
        """convert list to binary tree"""
        # final_tree = BinaryTree()
        for index in range(len(lst)):
            self.add_node_in_order(lst[index])
        return self

    def find_pre_order_index(self, value):
        """return the pre-order index of node"""
        pre_lst = self.to_list_pre_order()
        return pre_lst.index(value)

    def find_in_order_index(self, value):
        """return the in-order index of node"""
        in_lst = self.to_list_in_order()
        return in_lst.index(value)

    def find_post_order_index(self, value):
        """return the post-order index of node"""
        post_lst = self.to_list_post_order()
        return post_lst.index(value)

    def find_level_order_index(self, value):
        """return the level-order index of node"""
        level_lst = self.to_list_level_order()
        return level_lst.index(value)

    def filter(self):
        """filter un-int element"""
        lst = self.to_list_pre_order()
        result = []
        for i in range(len(lst)):
            if type(lst[i]) == int:
                result.append(lst[i])
        return result

    def map(self, f):
        if self.root is None:
            return None
        cur = self.root
        node_queue = list()
        node_queue.append(cur)
        while len(node_queue):
            cur = node_queue.pop(0)
            cur.value = f(cur.value)
            if cur.left is not None:
                node_queue.append(cur.left)
            if cur.right is not None:
                node_queue.append(cur.right)
        return self

    def reduce(self, f, initial_state=0):
        """return sum of the bt"""
        state = initial_state
        lst = self.to_list_pre_order()
        for i in range(len(lst)):
            state = f(state, lst[i])
        return state

    def empty(self):
        return None

    def concat(self,t1,t2):
        """concat two trees"""
        if not t1:
            return t2
        if not t2:
            return t1
        root = BinaryTreeNode(t1.value + t2.value)
        root.left = self.concat(t1.left, t2.left)
        root.right = self.concat(t1.right, t2.right)
        return root

    def equal(self,tree):
        """whether self is equal to tree"""
        root1 = self.root
        root2 = tree.root
        if root1 is None and root2 is None:
            return True
        if root1 is None and root2 is not None:
            return False
        if root1 is not None and root2 is None:
            return False
        if root1.value == root2.value:
            return BinaryTree(root1.left).equal(BinaryTree(root2.left)) and BinaryTree(root1.right).equal(BinaryTree(root2.right))
        else:
            return False

    def __iter__(self):
        """return iterator itself"""
        if self.root is None:
            self.cur = 0
            return self
        self.level_queue.append(self.root)
        self.cur += 1
        return self

    def __next__(self):
        """return next element or StopIteration"""
        if self.cur == 0:
            raise StopIteration
        if self.root.left is not None:
            self.level_queue.append(self.root.left)
        if self.root.right is not None:
            self.level_queue.append(self.root.right)
        tmp = self.level_queue[self.cur-1].value
        if self.cur < len(self.level_queue):
            self.root = self.level_queue[self.cur]
            self.cur += 1
        else:
            self.root = self.level_queue[0]
            self.cur = 0
        return tmp






