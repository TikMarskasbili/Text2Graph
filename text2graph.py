import networkx as nx
from collections import defaultdict
import re 
import matplotlib.pyplot as plt
import os


# 步骤1: 读取和解析文本文件
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        
        # 使用正则表达式替换非字母字符为空格
        text = re.sub(r'[^a-zA-Z]', ' ', text)
        
        # 将文本转换为小写并按空格分割
        words = text.lower().split()
    
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
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')  # 使用Graphviz的dot布局

    plt.figure(figsize=(10, 8))

    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', 
            font_size=10, font_weight='bold', arrows=True, arrowstyle='->', arrowsize=20)

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # 删除已有的图像文件
    if os.path.exists("text2graph.png"):
        os.remove("text2graph.png")

    # 保存新的图像
    plt.savefig("text2graph.png")

    plt.show()



# 步骤4: 查询桥接词
def find_bridge_words(G, word1, word2):
    if word1 not in G or word2 not in G:
        return f"No {word1} or {word2} in the graph!"
    
    bridge_words = []
    successors = list(G.successors(word1))
    predecessors = list(G.predecessors(word2))
    for successor in successors:
        if successor in predecessors:
            bridge_words.append(successor)
    
    if not bridge_words:
        return f"No bridge words from {word1} to {word2}!"
    else:
        return f"The bridge words from {word1} to {word2} are: {', '.join(bridge_words)}."


# 步骤5: 插入桥接词
def insert_bridge_words(text, G):
    words = text.lower().split()
    new_text = []

    for i in range(len(words) - 1):
        new_text.append(words[i])
        bridge_word = find_bridge_words(G, words[i], words[i + 1])
        if bridge_word:
            new_text.append(bridge_word)

    new_text.append(words[-1])  # 添加最后一个单词

    return ' '.join(new_text)

# 主函数
def main():
    file_path = 'poet.txt'  # 假设文本文件名为text.txt
    words = read_text_file(file_path)
    G = build_directed_graph(words)
    visualize_graph(G)
    word1 = input("Enter the first word: ").lower()
    word2 = input("Enter the second word: ").lower()
    
    result = find_bridge_words(G, word1, word2)
    print(result)

    new_text = input("Enter the new text: ")
    new_text_with_bridge_words = insert_bridge_words(new_text, G)
    print("Result with bridge words:", new_text_with_bridge_words)

if __name__ == '__main__':
    main()