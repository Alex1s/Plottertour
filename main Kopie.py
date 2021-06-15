import itertools
import random
from collections import namedtuple
from operator import itemgetter, attrgetter
from secrets import randbelow
import matplotlib.pyplot as plt
Point = namedtuple('Point', {'x': int, 'y': int})
from typing import List, Tuple

Plottertour = namedtuple('Plottertour', {'upper': List[Point], 'lower': List[Point]})
import numpy as np


NUM_POINTS = 5
MAX_VALUE = 20


def print_plottertour(tour: List[Point], max_x: int, max_y: int, hline: float = None, path_a=None, path_b=None) -> None:
    # linear = tour.upper[:-1] + tour.lower
    xs = list(map(itemgetter(0), tour))
    ys = list(map(itemgetter(1), tour))
    xs += [xs[0]]
    ys += [ys[0]]
    xs = np.array(xs)
    ys = np.array(ys)
    if len(xs) >= 1:
        plt.text(xs[0], ys[0], 'X', color='red')
    plt.xlim(0, max_x)
    plt.ylim(0, max_y)
    if hline is not None:
        plt.hlines(hline, 0, 10)

    plt.quiver(xs[:-1], ys[:-1], xs[1:] - xs[:-1], ys[1:] - ys[:-1], scale_units='xy', angles='xy', scale=1)
    if path_a is not None and path_b is not None:
        a_xs = np.array(list(map(attrgetter('x'), path_a)))
        a_ys = np.array(list(map(attrgetter('y'), path_a)))
        b_xs = np.array(list(map(attrgetter('x'), path_b)))
        b_ys = np.array(list(map(attrgetter('y'), path_b)))
        plt.quiver(a_xs[:-1], a_ys[:-1], a_xs[1:] - a_xs[:-1], a_ys[1:] - a_ys[:-1], scale_units='xy', angles='xy', scale=1, color='blue')
        plt.quiver(b_xs[:-1], b_ys[:-1], b_xs[1:] - b_xs[:-1], b_ys[1:] - b_ys[:-1], scale_units='xy', angles='xy', scale=1, color='red')
    plt.grid()
    plt.show()
    plt.close()


def plottertour_dandc(points: List[Point]) -> List[Point]:
    if len(points) <= 3:
        return points

    i = len(points) // 2
    left = points[:i]
    right = points[i:]
    tour_left = plottertour_dandc(left)
    tour_right = plottertour_dandc(right)
    print_plottertour(tour_left, MAX_VALUE, MAX_VALUE)
    print_plottertour(tour_right, MAX_VALUE, MAX_VALUE)

    if left[-1].y >= left[-2].y:
        left_upper = left[-1]
    else:
        left_upper = left[-2]
    index_left_upper = tour_left.index(left_upper)

    if right[0].y > right[1].y:
        right_upper = right[0]
    else:
        right_upper = right[1]
    index_right_upper = tour_right.index(right_upper)
    print(right_upper)


    result = tour_left[:index_left_upper + 1]
    result += tour_right[index_right_upper:] + tour_right[:index_right_upper]
    result += tour_left[index_left_upper + 1:]

    assert len(result) == len(points)
    return result


def plottertour(points: List[Point]) -> Tuple[List[Point], float]:
    points_sorted_y = sorted(points, key=itemgetter(1))
    y_min = points_sorted_y[0].y
    y_max = points_sorted_y[-1].y
    middle_line = (y_max - y_min) / 2
    middle_line += y_min
    points_upper = list(filter(lambda p: p.y >= middle_line, points))
    points_lower = list(filter(lambda p: p.y < middle_line, points))
    result = points_upper + list(reversed(points_lower))
    return result, middle_line


def plottertour_paths(points: List[Point]) -> Tuple[List[Point], List[Point], List[Point]]:
    points_sorted_x = sorted(points, key=attrgetter('x'))
    path_a = [points_sorted_x[0]]
    path_b = [points_sorted_x[0]]

    for point in points_sorted_x[1:]:
        tour_a = path_a + [point] + list(reversed(path_b))[:-1]
        tour_b = path_a + list(reversed(path_b + [point]))[:-1]
        if tour_weight(tour_a) > tour_weight(tour_b):
            path_b += [point]
        else:
            path_a += [point]
    return path_a + list(reversed(path_b))[:-1], path_a, path_b


def tour_weight(tour: List[Point]) -> int:
    sum = 0
    for i in range(len(tour)):
        sum += abs(tour[i].y - tour[(i + 1) % len(tour)].y)
    return sum


def is_valid_tour(tour: List[Point]) -> bool:
    tour_sorted = sorted(tour, key=itemgetter(0))
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


def optimal_tour(points: List[Point]) -> List[Point]:
    all_possible_tours = itertools.permutations(points, len(points))
    best_tour = None
    best_tour_weight = 999999999999999
    for tour in all_possible_tours:
        if is_valid_tour(tour):
            weight = tour_weight(tour)
            if weight < best_tour_weight:
                best_tour = tour
                best_tour_weight = weight
    return best_tour


def gen_points(max_value: int, num_points: int) -> List[Point]:
    xs = []
    ys = []
    while True:
        xs = []
        ys = []
        for _ in range(NUM_POINTS):
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


def isthatwrong() -> None:
    # points = gen_points(MAX_VALUE, NUM_POINTS)
    points = [Point(x=4, y=17), Point(x=13, y=17), Point(x=14, y=20), Point(x=16, y=12), Point(x=19, y=13)]
    best_tour = optimal_tour(points)
    print(best_tour)
    print(tour_weight(best_tour))
    print_plottertour(best_tour, MAX_VALUE, MAX_VALUE)

    my_tour = (Point(x=4, y=17), Point(x=13, y=17), Point(x=14, y=20), Point(x=19, y=13), Point(x=16, y=12))
    print(my_tour)
    print(tour_weight(my_tour))
    print_plottertour(my_tour, MAX_VALUE, MAX_VALUE)


def main_dandc() -> None:
    # points = gen_points(MAX_VALUE, NUM_POINTS)
    points = [Point(x=0, y=14), Point(x=7, y=6), Point(x=10, y=19), Point(x=15, y=1), Point(x=17, y=13)]
    print(points)
    best_tour = optimal_tour(points)
    print(best_tour)
    print(tour_weight(best_tour))
    print_plottertour(best_tour, MAX_VALUE, MAX_VALUE)

    dandc_tour = plottertour_dandc(points)
    print(dandc_tour)
    print(tour_weight(dandc_tour))
    print_plottertour(dandc_tour, MAX_VALUE, MAX_VALUE)


def main() -> None:
    points = gen_points(MAX_VALUE, NUM_POINTS)

    best_tour = optimal_tour(points)
    print(best_tour)
    print(tour_weight(best_tour))
    print_plottertour(best_tour, MAX_VALUE, MAX_VALUE)

    path_tour, path_a, path_b = plottertour_paths(points)
    print(path_tour)
    path_tour_weight = tour_weight(path_tour)
    print_plottertour(path_tour, MAX_VALUE, MAX_VALUE, path_a=path_a, path_b=path_b)
    print(f'{tour_weight(best_tour)} =? {path_tour_weight}')


if __name__ == '__main__':
    main_dandc()
    # main()
