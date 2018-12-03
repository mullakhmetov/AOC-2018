import re
import sys
from pprint import pprint
from collections import namedtuple


CLAIM_RE = re.compile(r'\#(\d+) @ (\d+)\,(\d+): (\d+)x(\d+)')
Claim = namedtuple('Claim', ['id', 'w_offset', 'h_offset', 'w', 'h', 'w_size', 'h_size'])


def increase_fabric_w(fabric, delta):
    for column in fabric:
        column.extend([0 for x in range(delta)])
    return fabric


def increase_fabric_h(fabric, delta):
    w = len(fabric[0])
    fabric.extend([0 for x in range(w)] for y in range(delta))
    return fabric


def resize_fabric(fabric, w, h):
    w_delta = w - len(fabric[0])
    if w_delta >= 0:
        fabric = increase_fabric_w(fabric, w_delta)
    h_delta = h - len(fabric)
    if h_delta >= 0:
        fabric = increase_fabric_h(fabric, h_delta)

    return fabric


def fill_fabric(fabric, w_offset, h_offset, w, h):
    start_w_slice = w_offset
    end_w_slice = start_w_slice + w
    start_h_slice = h_offset
    end_h_slice = start_h_slice + h
    for column in fabric[start_h_slice:end_h_slice]:
        # increase slice
        column[start_w_slice:end_w_slice] = [i + 1 for i in column[start_w_slice:end_w_slice]]

    return fabric


def has_overlap(fabric, w_offset, h_offset, w, h):
    start_w_slice = w_offset
    end_w_slice = start_w_slice + w
    start_h_slice = h_offset
    end_h_slice = start_h_slice + h
    for column in fabric[start_h_slice:end_h_slice]:
        # slice has no overlaps if it contains only 1's
        if column[start_w_slice:end_w_slice] != [1] * w:
            return True


def parse_claim(claim_data):
    c = CLAIM_RE.match(claim_data)
    id_, w_offset, h_offset, w, h = (int(i) for i in c.groups())
    w_size = w_offset + w
    h_size = h_offset + h
    return Claim(id_, w_offset, h_offset, w, h, w_size, h_size)


def main():
    with open('input.txt', 'r') as f:
        claims = [parse_claim(l.strip()) for l in f.readlines()]

    # don't want to cheating with numpy
    start_w = start_h = 10
    # as long as today leaderbord completed,
    # go visual way with matrix rather than optimized one storing coordinates in `defaultdict(int)`
    fabric = [[0 for x in range(start_w)] for y in range(start_h)]

    for claim in claims:
        fabric = resize_fabric(fabric, claim.w_size, claim.h_size)
        fabric = fill_fabric(fabric, claim.w_offset, claim.h_offset, claim.w, claim.h)

    res = 0
    for i in fabric:
        for j in i:
            if j > 1:
                res += 1

    print(f'overlaps: {res}')

    for claim in claims:
        if not has_overlap(fabric, claim.w_offset, claim.h_offset, claim.w, claim.h):
            print(f'unique claim: {claim.id}')
            sys.exit()


if __name__ == '__main__':
    main()
