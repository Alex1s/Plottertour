import itertools
from collections import namedtuple
from operator import attrgetter
from secrets import randbelow
from typing import List

import numpy as np
import matplotlib.pyplot as plt


Point = namedtuple('Point', {'x': int, 'y': int})


def print_plottertour(tour: List[Point],
                      max_x: int, max_y: int, path_a=None, path_b=None, title: str = None) -> None:
    xs = list(map(attrgetter('x'), tour))
    ys = list(map(attrgetter('y'), tour))
    xs += [xs[0]]
    ys += [ys[0]]
    xs = np.array(xs)
    ys = np.array(ys)
    if len(xs) >= 1:
        plt.text(xs[0], ys[0], 'X', color='red')
    plt.xlim(0, max_x)
    plt.ylim(0, max_y)
    plt.grid()
    if title is not None:
        plt.title(title)

    plt.quiver(xs[:-1], ys[:-1], xs[1:] - xs[:-1], ys[1:] - ys[:-1], scale_units='xy', angles='xy', scale=1)
    if path_a is not None and path_b is not None:
        a_xs = np.array(list(map(attrgetter('x'), path_a)))
        a_ys = np.array(list(map(attrgetter('y'), path_a)))
        b_xs = np.array(list(map(attrgetter('x'), path_b)))
        b_ys = np.array(list(map(attrgetter('y'), path_b)))
        plt.quiver(a_xs[:-1], a_ys[:-1], a_xs[1:] - a_xs[:-1], a_ys[1:] - a_ys[:-1],
                   scale_units='xy', angles='xy', scale=1, color='blue', label='Path A')
        plt.quiver(b_xs[:-1], b_ys[:-1], b_xs[1:] - b_xs[:-1], b_ys[1:] - b_ys[:-1],
                   scale_units='xy', angles='xy', scale=1, color='red', label='Path B')
        plt.suptitle('Path A: red; Path B: blue')

    plt.show()
    plt.close()


def gen_points(max_value: int, num_points: int) -> List[Point]:
    while True:
        xs = []
        ys = []
        for _ in range(num_points):
            xs.append(randbelow(max_value + 1))
            ys.append(randbelow(max_value + 1))

        continue_while = False
        for i in range(num_points):
            for j in range(num_points):
                if not continue_while and i != j:
                    if xs[i] == xs[j]:
                        xs = []
                        ys = []
                        continue_while = True
        if continue_while:
            continue
        break
    xs.sort()
    return list(map(lambda p: Point(p[0], p[1]), zip(xs, ys)))


def optimal_tour(points: List[Point]) -> List[Point]:
    all_possible_tours = itertools.permutations(points, len(points))
    best_tour = None
    best_tour_weight = 999999999999999
    for tour in all_possible_tours:
        if is_valid_tour(list(tour)):
            weight = tour_weight(list(tour))
            if weight < best_tour_weight:
                best_tour = tour
                best_tour_weight = weight
    return list(best_tour)


def optimal_tours(points: List[Point]) -> List[Point]:
    all_possible_tours = itertools.permutations(points, len(points))
    best_tours = []
    best_tour_weight = 999999999999999
    for tour in all_possible_tours:
        if is_valid_tour(list(tour)):
            weight = tour_weight(list(tour))
            if weight < best_tour_weight:
                best_tours = [tour]
                best_tour_weight = weight
            elif weight == best_tour_weight:
                best_tours.append(tour)
    return best_tours


def is_valid_tour(tour: List[Point]) -> bool:
    tour_sorted = list(sorted(tour, key=attrgetter('x')))
    smallest_x_point = tour_sorted[0]
    if tour[0] != smallest_x_point:
        return False

    ascending = True
    last_x = -1
    for point in tour:
        if ascending:
            if not point.x > last_x:
                ascending = False
        else:
            if not point.x < last_x:
                return False
        last_x = point.x
    return True


def tour_weight(tour: List[Point]) -> int:
    weight = 0
    for i in range(len(tour)):
        weight += abs(tour[i].y - tour[(i + 1) % len(tour)].y)
    return weight
