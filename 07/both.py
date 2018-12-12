import re
import heapq
from collections import namedtuple, defaultdict


# line example: Step C must be finished before step A can begin
step_re = re.compile(r'Step\s([A-Z]).+step\s([A-Z]).+')
Step = namedtuple('Step', ['name', 'parent'])

MAX_WORKERS = 5
BASE_TIME = 60


def parse_step(instruction):
    m = step_re.match(instruction)
    parent, name = m.groups()
    return Step(name, parent)


def get_indegrees(graph):
    # number of edges pointing to the node
    indegree_map = defaultdict(int)
    for k, children in graph.items():
        # set default value
        indegree_map[k]
        for c in children:
            indegree_map[c] += 1

    # these nodes have zero indegree
    zero_indegree = [k for k, v in indegree_map.items() if not v]
    # use heap to maintain lexicographical order
    heapq.heapify(zero_indegree)
    return indegree_map, zero_indegree


def topological_sort(graph):
    '''
    https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm
    '''
    indegree_map, zero_indegree = get_indegrees(graph)
    while zero_indegree:
        node = heapq.heappop(zero_indegree)
        for child in graph[node]:
            indegree_map[child] -= 1

            if indegree_map[child] == 0:
                heapq.heappush(zero_indegree, child)
                del indegree_map[child]
        yield node


def get_node_time(node):
    if not node:
        return 0
    return ord(node) - ord('A') + BASE_TIME + 1


def remove_node(nodes, node):
    for k, v in nodes.items():
        if node in v:
            v.remove(node)
            nodes[k] = v
    if node in nodes:
        del nodes[node]


def main():
    with open('input.txt', 'r') as f:
         instructions = [l.strip() for l in f.readlines()]

    steps = [parse_step(i) for i in instructions]

    graph = defaultdict(list)
    nodes = defaultdict(list)
    for step in steps:
        graph[step.parent].append(step.name)

        nodes[step.name].append(step.parent)
        nodes[step.parent]  # trigger default value

    # `graph` representation is dict like:
    # {'A': ['B', 'D'],
    #  'B': ['E'],
    #  'C': ['A', 'F'],
    #  'D': ['E'],
    #  'F': ['E']})
    #
    # where key is node and value is a list containing the nodes
    # that are connected by a direct arc from key node.
    #
    # `nodes` representation is reversed graph dict:
    # {'A': ['C'],
    #  'B': ['A'],
    #  'C': [],
    #  'D': ['A'],
    #  'E': ['B', 'D', 'F'],
    #  'F': ['C']})

    sorted_nodes = topological_sort(graph)
    part_1_result = ''.join(sorted_nodes)
    print(f'part 1: {part_1_result}')

    workers = {i: (None, None) for i in range(MAX_WORKERS)}

    current_time = 0
    while nodes:
        # remove finished tasks
        for k, (node, worker_time) in workers.items():
            if not node:
                continue

            if worker_time == current_time:
                workers[k] = (None, None)
                remove_node(nodes, node)

        # add new tasks
        for k, _ in workers.items():
            if _ != (None, None):
                continue

            ready_nodes = [n for n, children in nodes.items() if not children and n not in [n for n, _ in workers.values()]]
            if not ready_nodes:
                break

            node = ready_nodes.pop()
            time = get_node_time(node) + current_time
            workers[k] = node, time

        current_time += 1

    print(f'part 2: {current_time - 1}')


if __name__ == '__main__':
    main()
