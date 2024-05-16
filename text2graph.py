import networkx as nx
from collections import defaultdict


# 步骤1: 读取和解析文本文件
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
        # 清理文本，转换为小写，并按空格分割
        words = text.lower().replace('\n', ' ').split()
    return words


# 步骤2: 构建有向图
def build_directed_graph(words):
    G = nx.DiGraph()
    edge_count = defaultdict(int)
    for i in range(len(words) - 1):
        word1, word2 = words[i], words[i + 1]
        if G.has_edge(word1, word2):
            edge_count[(word1, word2)] += 1
        else:
            G.add_edge(word1, word2, weight=1)
            edge_count[(word1, word2)] = 1
            # 更新边的权重
    for edge, count in edge_count.items():
        G[edge[0]][edge[1]]['weight'] = count
    return G


# 步骤3: 展示生成的有向图 (需要Graphviz和pygraphviz)
def visualize_graph(G):
    import matplotlib.pyplot as plt
    nx.draw(G, with_labels=True)
    plt.show()


# 步骤5: 查询桥接词
def find_bridge_words(G, word1, word2):
    bridge_words = []
    successors = list(G.successors(word1))
    predecessors = list(G.predecessors(word2))
    for successor in successors:
        if successor in predecessors:
            bridge_words.append(successor)
    return bridge_words


# 主函数
def main():
    file_path = 'poet.txt'  # 假设文本文件名为text.txt
    words = read_text_file(file_path)
    G = build_directed_graph(words)
    visualize_graph(G)
    word1 = 'to'
    word2 = 'and'
    bridge_words = find_bridge_words(G, word1, word2)
    if not bridge_words:
        print("No bridge words from {} to {}!".format(word1, word2))
    else:
        print("The bridge words from {} to {} are: {}".format(word1, word2, ', '.join(bridge_words)))


if __name__ == '__main__':
    main()