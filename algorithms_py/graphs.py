def DFS(node, label):
    search_order = []
    stack = []
    processed = set() 
    stack.append(node)
    while stack:
        current_node = stack.pop()
        search_order.append(current_node.label)
        if current_node.label == label:
            return True, search_order
        if current_node not in processed:
            processed.add(current_node)
            for edge in sorted(current_node.edges, key=lambda edge: edge.node.label, reverse=True):
                if edge.node not in processed and edge.node not in stack:
                    stack.append(edge.node)
    return False, search_order


def BFS(node, label):
    search_order = []
    q = MyQueue()
    processed = set() 
    q.put(node)
    while not q.is_empty():
        current_node = q.get()
        search_order.append(current_node.label)
        if current_node.label == label:
            return current_node, search_order
        if current_node not in processed:
            processed.add(current_node)
            for edge in current_node.edges:
                if edge.node not in processed and not q.is_in_queue(edge.node):
                    q.put(edge.node)
    return None, search_order