import unittest
import networkx as nx
from text2graph import find_and_display_shortest_path, build_directed_graph, read_text_file

class TestFindAndDisplayShortestPath(unittest.TestCase):

    def setUp(self):
        # 创建一个图用于测试
        self.file_path = 'test.txt'  # 假设文本文件名为text.txt
        self.words = read_text_file(self.file_path)
        self.G = build_directed_graph(self.words)
        # 添加一些边和权重
        self.G.add_edge('A', 'B', weight=1)
        self.G.add_edge('B', 'C', weight=2)
        self.G.add_edge('A', 'C', weight=3)
        self.G.add_edge('C', 'D', weight=1)

    def test_normal_path(self):
        # 测试存在路径的情况
        words = ['A', 'D']
        expected_path = ['A', 'B', 'C', 'D']
        expected_length = 4
        path, length = find_and_display_shortest_path(self.G, words)
        self.assertEqual(path, expected_path)
        self.assertEqual(length, expected_length)

    def test_no_path(self):
        # 测试不存在路径的情况
        words = ['A', 'E']
        with self.assertRaises(nx.NetworkXNoPath):
            find_and_display_shortest_path(self.G, words)

    def test_single_node(self):
        # 测试只有一个节点的情况
        words = ['A']
        expected_path = ['A']
        expected_length = 0
        path, length = find_and_display_shortest_path(self.G, words)
        self.assertEqual(path, expected_path)
        self.assertEqual(length, expected_length)

    def test_nonexistent_node(self):
        # 测试输入的节点不在图中的情况
        words = ['X', 'Y']
        with self.assertRaises(ValueError):  # 假设函数在节点不存在时抛出ValueError
            find_and_display_shortest_path(self.G, words)

    # 可以继续添加更多的测试用例...

if __name__ == '__main__':
    unittest.main()