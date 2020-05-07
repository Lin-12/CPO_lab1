import unittest
from hypothesis import given
import hypothesis.strategies as st

from mutable_bt import *

class TestMutableList(unittest.TestCase):

    def test_size(self):
        self.assertEqual(binary_tree().size(),0)
        self.assertEqual(binary_tree(binary_tree_node(1)).size(),1)
        self.assertEqual(binary_tree().lst2bt([1,2,3]).size(),3)

    def test_pre2list(self):
        self.assertEqual(binary_tree().preorder2list(),None)
        self.assertEqual(binary_tree(binary_tree_node(2,binary_tree_node(3))).preorder2list(),[2,3])

    def test_in2list(self):
        self.assertEqual(binary_tree(binary_tree_node(2,binary_tree_node(3))).inorder2list(),[3,2])

    def test_post2list(self):
        self.assertEqual(binary_tree(binary_tree_node(2,binary_tree_node(3),binary_tree_node(4))).postorder2list(),[3,4,2])

    def test_add(self):
        bt = binary_tree()
        bt.add_node_in_order(1)
        self.assertEqual(bt.preorder2list(), [1])
        bt.add_node_in_order(2)
        self.assertEqual(bt.preorder2list(),[1,2])
        bt.add_node_in_order(3)
        self.assertEqual(bt.preorder2list(),[1,2,3])

    def test_remove(self):
        bt = binary_tree()
        for i in range(10):
            bt.add_node_in_order(i)
        bt.remove(2)
        self.assertNotIn(2, bt.preorder2list())

    def test_reduce(self):
        bt = binary_tree()
        for i in range(10):
            bt.add_node_in_order(i)
        self.assertEqual(bt.reduce(sum),45)

    def test_lst2bt(self):
        lst = [2,3,4]
        bt = binary_tree().lst2bt(lst)
        test_tree = binary_tree(binary_tree_node(2,binary_tree_node(3),binary_tree_node(4)))
        self.assertTrue(bt.isEqual(test_tree))

    def test_filter(self):
        bt = binary_tree()
        bt.add_node_in_order(1)
        bt.add_node_in_order(2)
        bt.add_node_in_order('1')
        bt.add_node_in_order(3)
        bt.add_node_in_order('2')
        self.assertEqual(bt.tree_filter(),[1,2,3])

    def test_map(self):
        self.assertEqual(binary_tree(binary_tree_node(3,binary_tree_node(4))).tree_map(f),[6,8])

    def test_concat(self):
        bt0 = binary_tree()
        bt0.add_node_in_order(1)
        bt0.add_node_in_order(2)
        bt1 = binary_tree()
        bt1.add_node_in_order(2)
        bt1.add_node_in_order(3)
        b = binary_tree()
        b = b.tree_mconcat(bt0.root, bt1.root)
        self.assertEqual(binary_tree(b).preorder2list(),[3,5])
        bt1.add_node_in_order(4)
        b = binary_tree()
        b = b.tree_mconcat(bt0.root, bt1.root)
        self.assertEqual(binary_tree(b).preorder2list(),[3,5,4])


if __name__ == '__main__':
    unittest.main()