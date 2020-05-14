import unittest

from hypothesis import given
import hypothesis.strategies as st

from mutable_bt import *


class TestMutableList(unittest.TestCase):
    def test_size(self):
        self.assertEqual(BinaryTree().size(), 0)
        self.assertEqual(BinaryTree(BinaryTreeNode(1)).size(), 1)
        self.assertEqual(BinaryTree().from_list([1, 2, 3]).size(), 3)

    def test_remove(self):
        bt = BinaryTree()
        for i in range(10):
            bt.add_node_in_order(i)
        bt.remove(2)
        self.assertNotIn(2, bt.to_list_pre_order())

    def test_add(self):
        bt = BinaryTree()
        bt.add_node_in_order(1)
        self.assertEqual(bt.to_list_pre_order(), [1])
        bt.add_node_in_order(2)
        self.assertEqual(bt.to_list_pre_order(), [1, 2])
        bt.add_node_in_order(3)
        self.assertEqual(bt.to_list_pre_order(), [1, 2, 3])

    def test_to_list_pre_order(self):
        self.assertEqual(BinaryTree().to_list_pre_order(), [])
        self.assertEqual(BinaryTree(BinaryTreeNode(2, BinaryTreeNode(3))).to_list_pre_order(), [2,3])
        self.assertEqual(BinaryTree(BinaryTreeNode(2, left=BinaryTreeNode(3, right=BinaryTreeNode(5)),
                                                   right=BinaryTreeNode(4, left=BinaryTreeNode(6)))).to_list_pre_order()
                         , [2, 3, 5, 4, 6])

    def test_to_list_in_order(self):
        self.assertEqual(BinaryTree().to_list_in_order(), [])
        self.assertEqual(BinaryTree(BinaryTreeNode(2, BinaryTreeNode(3))).to_list_in_order(), [3,2])
        self.assertEqual(BinaryTree(BinaryTreeNode(2, left=BinaryTreeNode(3, right=BinaryTreeNode(5)),
                                                   right=BinaryTreeNode(4, left=BinaryTreeNode(6)))).to_list_in_order(),
                         [3, 5, 2, 6, 4])

    def test_to_list_post_order(self):
        self.assertEqual(BinaryTree().to_list_post_order(), [])
        self.assertEqual(BinaryTree(BinaryTreeNode(2, BinaryTreeNode(3))).to_list_post_order(), [3,2])
        self.assertEqual(BinaryTree(BinaryTreeNode(2, left=BinaryTreeNode(3, right=BinaryTreeNode(5)),
                                                   right=BinaryTreeNode(4, left=BinaryTreeNode(6)))).to_list_post_order()
                         , [5, 3, 6, 4, 2])

    def test_to_list_level_order(self):
        self.assertEqual(BinaryTree().to_list_level_order(), [])
        self.assertEqual(BinaryTree(BinaryTreeNode(2, BinaryTreeNode(3))).to_list_level_order(), [2, 3])
        self.assertEqual(BinaryTree(BinaryTreeNode(2, left=BinaryTreeNode(3, right=BinaryTreeNode(5)),
                                                   right=BinaryTreeNode(4, left=BinaryTreeNode(6)))).to_list_level_order()
                         , [2, 3, 4, 5, 6])

    def test_from_list(self):
        lst = [2, 3, 4]
        bt = BinaryTree().from_list(lst)
        test_tree = BinaryTree(BinaryTreeNode(2, BinaryTreeNode(3), BinaryTreeNode(4)))
        self.assertTrue(bt.equal(test_tree))
        test_data = [
            [],
            [1,2],
            [1,2,3,4,5]
        ]
        for e in test_data:
            lst = BinaryTree()
            lst.from_list(e)
            self.assertEqual(lst.to_list_level_order(), e)

    def test_reduce(self):
        # sum of empty list
        bt = BinaryTree()
        self.assertEqual(bt.reduce(lambda st, e: st + e, 0), 0)

        # sum of list
        bt = BinaryTree()
        bt.from_list([1, 2, 3])
        self.assertEqual(bt.reduce(lambda st, e: st + e, 0), 6)

        # size
        test_data = [
            [],
            [1],
            [1, 2]
        ]
        for e in test_data:
            bt = BinaryTree()
            bt = bt.from_list(e)
            self.assertEqual(bt.reduce(lambda st, _: st + 1, 0), bt.size())

    def test_map(self):
        bt = BinaryTree()
        self.assertIsNone(bt.map(str))

        bt = BinaryTree()
        bt = bt.from_list([1, 2, 3])
        bt.map(str)
        self.assertEqual(bt.to_list_level_order(), ["1", "2", "3"])

        bt = BinaryTree()
        bt.from_list([1, 2, 3])
        bt.map(lambda x: x + 1)
        self.assertEqual(bt.to_list_level_order(), [2, 3, 4])

    def test_filter(self):
        bt = BinaryTree()
        bt.add_node_in_order(1)
        bt.add_node_in_order(2)
        bt.add_node_in_order('1')
        bt.add_node_in_order(3)
        bt.add_node_in_order('2')
        self.assertEqual(bt.filter(), [1, 2, 3])

    def test_concat(self):
        bt0 = BinaryTree()
        bt0.add_node_in_order(1)
        bt0.add_node_in_order(2)
        bt1 = BinaryTree()
        bt1.add_node_in_order(2)
        bt1.add_node_in_order(3)
        b = BinaryTree()
        b = b.concat(bt0.root, bt1.root)
        self.assertEqual(BinaryTree(b).to_list_pre_order(), [3, 5])
        bt1.add_node_in_order(4)
        b = BinaryTree()
        b = b.concat(bt0.root, bt1.root)
        self.assertEqual(BinaryTree(b).to_list_pre_order(), [3, 5, 4])

    @given(st.lists(st.integers()))
    def test_from_list_to_list_equality(self, a):
        bt1 = BinaryTree()
        bt1 = bt1.from_list(a)
        bt2 = bt1.to_list_level_order()
        self.assertEqual(a, bt2)

    @given(st.lists(st.integers()))
    def test_python_len_and_bt_size_equality(self,a):
        bt = BinaryTree()
        bt = bt.from_list(a)
        self.assertEqual(bt.size(),len(a))

    @given(st.lists(st.integers()))
    def test_monoid_identity(self, lst):
        """Identity element `a==0+a==a+0`"""
        bt1 = BinaryTree().from_list(lst)
        bt2 = BinaryTree()
        bt_concat = BinaryTree()
        self.assertEqual(BinaryTree(bt_concat.concat(bt1.root, bt2.empty())).to_list_level_order(), lst)
        self.assertEqual(BinaryTree(bt_concat.concat(bt2.empty(), bt1.root)).to_list_level_order(), lst)

    @given(a=st.lists(st.integers()), b=st.lists(st.integers()), c=st.lists(st.integers()))
    def test_monoid_associativity(self, a, b, c):
        """Associativity `(a+b)+c == a+(b+c)`"""
        bt_a = BinaryTree().from_list(a)
        bt_b = BinaryTree().from_list(b)
        bt_c = BinaryTree().from_list(c)

        # (a+b)+c
        bt_test1 = BinaryTree(BinaryTree().concat(BinaryTree().concat(bt_a.root, bt_b.root), bt_c.root))
        # a+(b+c)
        bt_test2 = BinaryTree(BinaryTree().concat(bt_a.root, BinaryTree().concat(bt_b.root, bt_c.root)))
        self.assertEqual(bt_test1.to_list_level_order(), bt_test2.to_list_level_order())

    def test_iter(self):
        x = [1, 2, 3]
        bt = BinaryTree()
        bt = bt.from_list(x)
        tmp = []
        for e in bt:
            tmp.append(e)
        self.assertEqual(x, tmp)
        self.assertEqual(bt.to_list_level_order(), tmp)

        i = iter(BinaryTree())
        self.assertRaises(StopIteration, lambda: next(i))


if __name__ == '__main__':
    unittest.main()
