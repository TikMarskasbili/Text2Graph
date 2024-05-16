import networkx as nx
from collections import defaultdict
import re 


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

    plt.figure(figsize=(10, 8))  # 设置图形大小

    # 绘制节点和边
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', 
            font_size=10, font_weight='bold', arrows=True, arrowstyle='->', arrowsize=20)

    # 为每条边添加权重标签
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.show()  # 显示图形


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