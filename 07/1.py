import re
import heapq
from itertools import count
from collections import namedtuple, defaultdict

from pprint import pprint


# line example: Step C must be finished before step A can begin
step_re = re.compile(r'Step\s([A-Z]).+step\s([A-Z]).+')
Step = namedtuple('Step', ['name', 'parent'])

MAX_WORKERS = 2


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
    return ord(node) - 64


def main():
    with open('input.txt', 'r') as f:
         instructions = [l.strip() for l in f.readlines()]

    steps = [parse_step(i) for i in instructions]

    nodes = set()
    graph = defaultdict(list)
    for step in steps:
        graph[step.parent].append(step.name)

        nodes.update((step.name, step.parent))

    # graph representation is dict like:
    #
    # {'A': ['B', 'D'],
    #  'B': ['E'],
    #  'C': ['A', 'F'],
    #  'D': ['E'],
    #  'F': ['E']})
    #
    # where key is node and value is a list containing the nodes
    # that are connected by a direct arc from key node.

    part_1_result = ''.join(topological_sort(graph))
    print(f'part 1: {part_1_result}')


if __name__ == '__main__':
    main()
