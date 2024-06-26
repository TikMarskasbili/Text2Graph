import unittest
import networkx as nx
import random
from text2graph import read_text_file,build_directed_graph,random_traversal

class TestGraphTraversal(unittest.TestCase):

    def test_empty_graph(self):
        # 当图为空时。
        G = nx.DiGraph()
        start_node = None
        visited_nodes, visited_edges = random_traversal(G, start_node)
        
        self.assertEqual(visited_nodes, [])
        self.assertEqual(visited_edges, [])

    def test_multiple_nodes_edges(self):
        # 当节点有多条边时
        words = read_text_file('test.txt')
        G = build_directed_graph(words)
        start_node = "new"
        visited_nodes, visited_edges = random_traversal(G, start_node)
        
        self.assertGreater(len(visited_nodes), 0)
        self.assertGreater(len(visited_edges), 0)

    def test_visited_edge_stopping(self):
        # 测试回环停止
        G = nx.DiGraph()
        G.add_edge("a", "b", weight=1)
        G.add_edge("b", "c", weight=1)
        G.add_edge("c", "a", weight=1)
        
        start_node = "a"
        visited_nodes, visited_edges = random_traversal(G, start_node)
        
        self.assertEqual(len(visited_nodes), 3)  # 因为最后一条边使得循环回到起点，导致停止
        self.assertEqual(len(visited_edges), 2)

    def test_random_start_node(self):
        # 输入为空时
        words = read_text_file('test.txt')
        G = build_directed_graph(words)
        start_node = None
        visited_nodes, visited_edges = random_traversal(G, start_node)
        
        self.assertIn(visited_nodes[0], words)
        self.assertGreater(len(visited_nodes), 0)
        self.assertGreater(len(visited_edges), 0)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(TestGraphTraversal))
