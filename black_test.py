import unittest
import networkx as nx


def find_and_display_shortest_path(G, input_str=None):
# 修改 find_and_display_shortest_path 函数以接受输入参数并返回结果
    output = []
    if input_str is None:
        input_str = input("输入一个或两个单词，并用空格分开: ").strip().lower()

    words = input_str.split()

    if len(words) == 1:
        word1 = words[0]
        if word1 not in G:
            output.append(f"{word1} 不在图中!")
            return output
        output.append(f"最短路径从 {word1} 到其他所有节点:")
        for target in G.nodes:
            if target != word1:
                try:
                    shortest_path = nx.shortest_path(G, source=word1, target=target, weight='weight')
                    path_length = nx.shortest_path_length(G, source=word1, target=target, weight='weight')
                    output.append(f"最短路径从 {word1} 到 {target} 是: {' -> '.join(shortest_path)} (Length: {path_length})")
                except nx.NetworkXNoPath:
                    output.append(f"没有路径从 {word1} 到 {target}!")
    elif len(words) == 2:
        word1, word2 = words
        if word1 not in G or word2 not in G:
            output.append(f" {word1} 或 {word2} 不在图中!")
            return output

        try:
            shortest_path = nx.shortest_path(G, source=word1, target=word2, weight='weight')
            path_length = nx.shortest_path_length(G, source=word1, target=word2, weight='weight')
            output.append(f"最短路径从 {word1} 到 {word2} 是: {' -> '.join(shortest_path)} (Length: {path_length})")
        except nx.NetworkXNoPath:
            output.append(f"没有路径从 {word1} 到 {word2}!")
    else:
        output.append("请输入一个或两个单词.")
    
    return output

class TestFindAndDisplayShortestPath(unittest.TestCase):
    def setUp(self):
        # 创建一个示例图
        self.G = nx.DiGraph()
        edges = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "e"), ("e", "f"), ("g", "h")]
        for edge in edges:
            self.G.add_edge(edge[0], edge[1], weight=1)

    def test_single_word_in_graph(self):
        input_words = "a"
        expected_output = [
            "最短路径从 a 到其他所有节点:",
            "最短路径从 a 到 b 是: a -> b (Length: 1)",
            "最短路径从 a 到 c 是: a -> b -> c (Length: 2)",
            "最短路径从 a 到 d 是: a -> b -> c -> d (Length: 3)",
            "最短路径从 a 到 e 是: a -> b -> c -> d -> e (Length: 4)",
            "最短路径从 a 到 f 是: a -> b -> c -> d -> e -> f (Length: 5)",
            "没有路径从 a 到 g!",
            "没有路径从 a 到 h!"
        ]
        result = find_and_display_shortest_path(self.G, input_words)
        self.assertEqual(result, expected_output, f"Failed on input: '{input_words}'\nExpected: {expected_output}\nGot: {result}")

    def test_two_words_in_graph(self):
        input_words = "a b"
        expected_output = ["最短路径从 a 到 b 是: a -> b (Length: 1)"]
        result = find_and_display_shortest_path(self.G, input_words)
        self.assertEqual(result, expected_output, f"Failed on input: '{input_words}'\nExpected: {expected_output}\nGot: {result}")

    def test_single_word_not_in_graph(self):
        input_words = "x"
        expected_output = ["x 不在图中!"]
        result = find_and_display_shortest_path(self.G, input_words)
        self.assertEqual(result, expected_output, f"Failed on input: '{input_words}'\nExpected: {expected_output}\nGot: {result}")

    def test_two_words_not_in_graph(self):
        input_words = "x y"
        expected_output = [" x 或 y 不在图中!"]
        result = find_and_display_shortest_path(self.G, input_words)
        self.assertEqual(result, expected_output, f"Failed on input: '{input_words}'\nExpected: {expected_output}\nGot: {result}")

    def test_one_word_in_graph_one_not(self):
        input_words = "a x"
        expected_output = [" a 或 x 不在图中!"]
        result = find_and_display_shortest_path(self.G, input_words)
        self.assertEqual(result, expected_output, f"Failed on input: '{input_words}'\nExpected: {expected_output}\nGot: {result}")

    def test_empty_input(self):
        input_words = ""
        expected_output = ["请输入一个或两个单词."]
        result = find_and_display_shortest_path(self.G, input_words)
        self.assertEqual(result, expected_output, f"Failed on input: '{input_words}'\nExpected: {expected_output}\nGot: {result}")

    def test_three_or_more_words(self):
        input_words = "a b c"
        expected_output = ["请输入一个或两个单词."]
        result = find_and_display_shortest_path(self.G, input_words)
        self.assertEqual(result, expected_output, f"Failed on input: '{input_words}'\nExpected: {expected_output}\nGot: {result}")

    def test_single_letter(self):
        input_words = "a"
        expected_output = [
            "最短路径从 a 到其他所有节点:",
            "最短路径从 a 到 b 是: a -> b (Length: 1)",
            "最短路径从 a 到 c 是: a -> b -> c (Length: 2)",
            "最短路径从 a 到 d 是: a -> b -> c -> d (Length: 3)",
            "最短路径从 a 到 e 是: a -> b -> c -> d -> e (Length: 4)",
            "最短路径从 a 到 f 是: a -> b -> c -> d -> e -> f (Length: 5)",
            "没有路径从 a 到 g!",
            "没有路径从 a 到 h!"
        ]
        result = find_and_display_shortest_path(self.G, input_words)
        self.assertEqual(result, expected_output, f"Failed on input: '{input_words}'\nExpected: {expected_output}\nGot: {result}")

    def test_longest_word(self):
        longest_word = "supercalifragilisticexpialidocious"
        input_words = longest_word
        expected_output = [f"{longest_word} 不在图中!"]
        result = find_and_display_shortest_path(self.G, input_words)
        self.assertEqual(result, expected_output, f"Failed on input: '{input_words}'\nExpected: {expected_output}\nGot: {result}")

if __name__ == '__main__':
    # 使用 verbosity=2 来获得详细输出
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(TestFindAndDisplayShortestPath))
