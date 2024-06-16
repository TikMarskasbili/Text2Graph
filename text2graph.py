import os
import random
import re
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx


def read_text_file(file_path):
    # 步骤1: 读取和解析文本文件
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        # 使用正则表达式替换非字母字符为空格
        text = re.sub(r'[^a-zA-Z]', ' ', text)
        # 将文本转换为小写并按空格分割
        words = text.lower().split()
    return words


def build_directed_graph(words):
    # 步骤2: 构建有向图
    graph_gen = nx.DiGraph()
    edge_count = defaultdict(int)
    for i in range(len(words) - 1):
        word1, word2 = words[i], words[i + 1]
        if graph_gen.has_edge(word1, word2):
            edge_count[(word1, word2)] += 1
        else:
            graph_gen.add_edge(word1, word2, weight=1)
            edge_count[(word1, word2)] = 1
            # 更新边的权重
    for edge, count in edge_count.items():
        graph_gen[edge[0]][edge[1]]['weight'] = count
    return graph_gen


def visualize_graph(graph_gen):
    # 步骤3: 展示生成的有向图 (需要Graphviz和pygraphviz)
    pos = nx.nx_agraph.graphviz_layout(graph_gen, prog='dot')  # 使用Graphviz的dot布局

    plt.figure(figsize=(10, 8))

    nx.draw(graph_gen, pos, with_labels=True, node_size=3000,
            node_color='lightblue',
            font_size=10,
            font_weight='bold',
            arrows=True, arrowstyle='->',
            arrowsize=20)
    edge_labels = nx.get_edge_attributes(graph_gen, 'weight')
    nx.draw_networkx_edge_labels(graph_gen, pos, edge_labels=edge_labels)

    # 删除已有的图像文件
    if os.path.exists("text2graph.png"):
        os.remove("text2graph.png")

    # 保存新的图像
    plt.savefig("text2graph.png")

    plt.show()


def find_bridge_words(graph_gen, word1, word2):
    # 步骤4: 查询桥接词
    if word1 not in graph_gen or word2 not in graph_gen:
        return f"No {word1} or {word2} in the graph!"
    bridge_words = []
    successors = list(graph_gen.successors(word1))
    predecessors = list(graph_gen.predecessors(word2))
    for successor in successors:
        if successor in predecessors:
            bridge_words.append(successor)
    if not bridge_words:
        return f"无桥接词从 {word1} 到 {word2}!"
    return f"桥接词从 {word1} 到 {word2} 是: {', '.join(bridge_words)}."



def insert_bridge_words(text, graph_gen):
    # 步骤5: 插入桥接词
    words = text.lower().split()
    new_text = []
    i = 0
    while i < len(words) - 1:
        word1, word2 = words[i], words[i + 1]
        # 检查单词对是否在图中，并且存在桥接词
        if word1 not in graph_gen or word2 not in graph_gen:
            new_text.append(word1)
            i += 1
            continue
        bridge_words = [
            node for node in graph_gen.neighbors(word1)
            if graph_gen.has_edge(node, word2)
        ]
        # 如果存在桥接词，随机选择一个插入
        if bridge_words:
            bridge_word = random.choice(bridge_words)
            new_text.append(word1)
            new_text.append(bridge_word)
        else:
            new_text.append(word1)
        # 更新索引
        i += 1
    # 处理最后一个单词
    if i == len(words) - 1:
        new_text.append(words[-1])
    return ' '.join(new_text)


def find_and_display_shortest_path(graph_gen, input_str=None):
    # 步骤6：最短路径
    output = []
    if input_str is None:
        input_str = input("输入一个或两个单词，并用空格分开: ").strip().lower()
    words = input_str.split()
    if len(words) == 1:
        word1 = words[0]
        if word1 not in graph_gen:
            output.append(f"{word1} 不在图中!")
            return output
        output.append(f"最短路径从 {word1} 到其他所有节点:")
        for target in graph_gen.nodes:
            if target != word1:
                try:
                    shortest_path = nx.shortest_path(
                        graph_gen, source=word1, target=target, weight='weight'
                    )
                    path_length = nx.shortest_path_length(
                        graph_gen, source=word1, target=target, weight='weight'
                    )
                    output.append(
                        f"最短路径从 {word1} 到 {target} 是: "
                        f"{' -> '.join(shortest_path)} (Length: {path_length})"
                    )
                except nx.NetworkXNoPath:
                    output.append(f"没有路径从{word1} 到 {target}!")
    elif len(words) == 2:
        word1, word2 = words
        if word1 not in graph_gen or word2 not in graph_gen:
            output.append(f" {word1} 或 {word2} 不在图中!")
            return output
        try:
            shortest_path = nx.shortest_path(
                graph_gen, source=word1, target=word2, weight='weight'
            )
            path_length = nx.shortest_path_length(
                graph_gen, source=word1, target=word2, weight='weight'
            )
            output.append(
                        f"最短路径从 {word1} 到 {word2} 是: "
                        f"{' -> '.join(shortest_path)} (Length: {path_length})"
                    )
        except nx.NetworkXNoPath:
            output.append(f"没有路径从 {word1} 到 {word2}!")
    else:
        output.append("请输入一个或两个单词.")
    return output


def random_traversal(graph_gen, start_node=None):
    # 步骤7：随机游走
    if not graph_gen.nodes:  # 如果图为空，返回空列表
        return [], []
    if start_node is None or start_node not in graph_gen:
        # 如果没有指定起始节点，或指定的起始节点不在图中，则随机选择一个
        start_node = random.choice(list(graph_gen.nodes))
    # 记录已访问的节点和边
    visited_nodes = [start_node]
    visited_edges = []
    current_node = start_node
    visited_set = set(visited_nodes)
    while True:
        # 获取当前节点的所有出边
        out_edges = list(graph_gen.out_edges(current_node, data=True))
        if not out_edges:
            # 如果没有出边，则停止遍历
            break
        # 从出边中随机选择一条
        chosen_edge = random.choice(out_edges)
        chosen_node = chosen_edge[1]
        # 如果该边已经访问过，则停止遍历
        if (current_node, chosen_node, chosen_edge[2]) in visited_edges or \
           (chosen_node, current_node, chosen_edge[2]) in visited_edges:
            break
        if chosen_node in visited_set:
            break
        # 添加到已访问的节点和边中
        visited_nodes.append(chosen_node)
        visited_edges.append((current_node, chosen_node, chosen_edge[2]))
        # 更新当前节点
        current_node = chosen_node
    return visited_nodes, visited_edges


def ui(graph_gen):
    # UI 界面
    while True:
        print("------->1、查询桥接词\n\t2、插入桥接词\n\t3、计算最短路径\n\t4、随机游走\n\texit、退出")
        choice = input("--->")
        if choice == '1':
            word1 = input("--->输入第一个词：").lower()
            word2 = input("--->输入第二个词: ").lower()
            result = find_bridge_words(graph_gen, word1, word2)
            print(result)
        elif choice == '2':
            new_text = input("--->输入一段新文本: ")
            new_text_with_bridge_words = insert_bridge_words(new_text, graph_gen)
            print("--->带有桥接词的结果是：", new_text_with_bridge_words)
        elif choice == '3':
            print(find_and_display_shortest_path(graph_gen))
        elif choice == '4':
            start_node = input("--->输入图中任一单词（可选）：").strip().lower()
            if start_node == "":
                start_node = None
            visited_nodes = random_traversal(graph_gen, start_node)
            # 将遍历结果输出为文本
            traversal_text = ' '.join(visited_nodes)
            print(traversal_text)
        elif choice == 'exit':
            break


def main():
    # 主函数
    file_path = 'test.txt'  # 假设文本文件名为text.txt
    words = read_text_file(file_path)
    graph_gen = build_directed_graph(words)
    visualize_graph(graph_gen)
    ui(graph_gen)


if __name__ == '__main__':
    main()
