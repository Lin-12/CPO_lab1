class binary_tree_node(object):
    def __init__(self,value=-1,left=None,right=None):
        self.value = value
        self.left = left
        self.right = right

    def get_value(self):
        """return node.element"""
        return self.value
    def __eq__(self, other):
        if self is None and other is not None:
            return True
        if self is None and other is not None:
            return False
        if self is None and other is not None:
            return False
        if self.value == other.value:
            return self.left.__eq__(other.left) and self.right.__eq__(other.right)
        else:
            return False
def create_new_root(node):
    if node is None:
        return None
    new_root = binary_tree_node(node.value)
    new_root.left = create_new_root(node.left)
    new_root.right = create_new_root(node.right)
    return new_root

def im_size(node):
    if node is None:
        return 0
    else:
        return 1+im_size(node.left)+im_size(node.right)

def add(root,value):
    new_node = binary_tree_node(value)
    if root is None:
        root = new_node
    node_queue = []
    node_queue.append(root)
    while True:
        if node_queue == []:
            return False
        node = node_queue.pop(0)
        if node.left is None:
            node.left = new_node
            return True

        elif node.right is None:
            node.right = new_node
            return True
        else:
            node_queue.append(node.left)
            node_queue.append(node.right)


def mempty():
    return None
"""
def preOrderTraverse(node):
    listp=[]
    if node is None:
        return None
    listp.append(node.value)
    preOrderTraverse(node.left)
    preOrderTraverse(node.right)

    return listp
"""
def preOrderTraverse(root):
    if root is None:
        return []
    result=[root.value]
    left_lst = preOrderTraverse(root.left)
    right_lst = preOrderTraverse(root.right)
    """"
    if left_lst is None and right_lst is None:
        return [root.value]
    if left_lst is None:
        return [root.value]+right_lst
    if right_lst is None:
        return [root.value]+left_lst
    """
    return result+left_lst+right_lst


"""
def to_list(node,s,lst):
    if s <= len(lst)-1:
        if node is not None:
            lst[s]=node.value
        else:
            lst[s]=None
            return
        to_list(node.left,(s<<1)+1,lst)
        to_list(node.right,(s<<1)+2,lst)
    else:
        return
"""
def to_list(root):
    res=[]
    if root.value is None:
        return res
    stack=[root]
    while stack:
        temp=stack.pop(0)
        if temp.value is not None:
            res.append(temp.value)
        else:
            res.append(None)
        if temp.left:
            stack.append(temp.left)
        if temp.right:
            stack.append(temp.right)
    return res

def from_list(list):
    root=binary_tree_node(list[0])
    for i,j in enumerate(list[1:]):
        add(root,j)
    return  root

def find_maxval(root,maxval=0):
    if root is None:
        return maxval
    l_max=find_maxval(root.left)
    r_max=find_maxval(root.right)
    return max(l_max,r_max,root.value)


def f(value):
    if type(value) == int:
        value = value * 2
    return value


def reduce_fuc(s, a):
    if type(a) == int and type(s) == int:
        return s + a
    else:
        return s

def filter_func(lst):
    new_list = []
    for i in range(len(lst)):
        if type(lst[i]) == int:
            new_list.append(lst[i])
    return new_list

def map(node,f):
    listmap=preOrderTraverse(node)
    for i in range(len(listmap)):
        listmap[i] = f(listmap[i])
    return listmap

def fliter(node,func):
    listfl = preOrderTraverse(node)
    return func(listfl)

def reduce(node,reduce_fuc):
    listre=preOrderTraverse(node)
    sum=0

    for i in range(len(listre)):
        sum=reduce_fuc(sum,listre[i])
    return sum

def mconcat(node1,node2):
    if node1 is None:
        return node2
    if node2 is None:
        return node1
    node1.value = node1.value + node2.value  # 获得当前结点
    node1.left = mconcat(node1.left, node2.left)  # 融合左子树
    node1.right = mconcat(node1.right, node2.right)
    return node1

def get_parent(root, value):
    '''
    找到 value 的父节点
    '''
    if root.value == value:
        return None  # 根节点没有父节点
    tmp = [root]
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

def delete(root, value):
    '''
    Remove an element from the binary tree
     First get the parent node of the node item to be deleted
     If the parent node is not empty,
     Determine the left and right subtrees of item
     If the left subtree is empty, then determine whether item is the left child or the right child of the parent node. If it is a left child, point the left pointer of the parent node to the right subtree of the item, otherwise point the right pointer of the parent node to the right of item Subtree
     If the right subtree is empty, then determine whether item is the left child or right child of the parent node. If it is a left child, point the left pointer of the parent node to the left child tree of item, otherwise, point the right pointer of the parent node to the left of item Subtree
     If the left and right subtrees are not empty, find the leftmost leaf node x in the right subtree and replace x with the node to be deleted.
     Delete successfully, return True
     Delete failed, return False
    '''
    if root is None:
        return False
    parent = get_parent(root,value)
    if parent:
        del_node = parent.left if parent.left.value == value else parent.right
        if del_node.left is None:
            if parent.left.value == value:
                parent.left = del_node.right
            else:
                parent.right = del_node.right
            del del_node
            return True
        elif del_node.right is None:
            if parent.left.value == value:
                parent.left = del_node.left
            else:
                parent.right = del_node.left
            del del_node
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
                while tmp_next.left:
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
            del del_node
            return True
    else:
        return False


root0 = binary_tree_node(1)
root1 = binary_tree_node(1, binary_tree_node(2,binary_tree_node(3)),binary_tree_node(4))
print(im_size(root0))
print(im_size(root1))
print(preOrderTraverse(root1))
print(find_maxval(root1))
print(map(root1,f))
print(fliter(root1,filter_func))
print(reduce(root1,reduce_fuc))
print(mconcat(root0,root1))
print(get_parent(root1,3))
print(delete(root1,3))
print(to_list(root1))
print(to_list(from_list([1,2,3,4])))