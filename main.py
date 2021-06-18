from utils import *
from typing import Tuple
from os import environ


NUM_POINTS = 10
MAX_VALUE = 10


def paths_to_tour(path_a: List[Point], path_b: List[Point], all_points_sorted: List[Point]):
    return [all_points_sorted[0]] + path_a + [all_points_sorted[-1]] + list(reversed(path_b))


def insert_at_index(path_a: List[Point], path_b: List[Point], i: int, point: Point) -> Tuple[List[Point], List[Point]]:
    path_a = path_a[:]
    path_b = path_b[:]

    path_b += path_a[i:]
    path_b.sort(key=attrgetter('x'))

    path_a = path_a[:i]
    path_a.append(point)

    return path_a, path_b


def insert_at_index_fast(path_a: List[Point], path_b: List[Point], i: int, point: Point) -> Tuple[List[Point], List[Point]]:
    new_path_a = []
    for j in range(i):
        new_path_a.append(path_a[j])
    new_path_a.append(point)

    rest_of_a = []
    for j in range(i, len(path_a)):
        rest_of_a.append(path_a[j])

    new_b = []
    j_path_b = 0
    j_rest_of_a = 0
    for _ in range(len(path_b) + len(rest_of_a)):
        if j_path_b == len(path_b):  # all elements from path_b used
            new_b.append(rest_of_a[j_rest_of_a])
            j_rest_of_a += 1
            continue
        if j_rest_of_a == len(rest_of_a):  # all elements from rest_of_a used
            new_b.append(path_b[j_path_b])
            j_path_b += 1
            continue

        # else take the smaller of the two to have them ordered
        if path_b[j_path_b].x < rest_of_a[j_rest_of_a].x: # next element in path b is the smaller one
            new_b.append(path_b[j_path_b])
            j_path_b += 1
            continue
        else:  # next element in rest_of_a is smaller
            new_b.append(rest_of_a[j_rest_of_a])
            j_rest_of_a += 1

    return new_path_a, new_b



def plottertour_paths(points: List[Point]) -> Tuple[List[Point], List[Point], List[Point]]:
    if len(points) <= 1:
        return points, points, points
    if len(points) == 2:
        return points, points, list(reversed(points))

    points = sorted(points, key=attrgetter('x'))
    path_a = []
    path_b = []

    best_path_a = None
    best_path_b = None
    for point in points[1:-1]:
        best_weight = None

        for i in range(len(path_a) + 1):
            potential_better_a, potential_better_b = insert_at_index_fast(path_a, path_b, i, point)
            potential_better_tour = paths_to_tour(potential_better_a, potential_better_b, points)
            potential_better_weight = tour_weight(potential_better_tour)

            if 'DEBUG' in environ:
                print(f'Potential Path A: {potential_better_a}')
                print(f'Potential Path B: {potential_better_b}')
                print_plottertour(potential_better_tour, MAX_VALUE, MAX_VALUE,
                                  path_a=[points[0]] + potential_better_a + [points[-1]],
                                  path_b=[points[0]] + potential_better_b + [points[-1]],
                                  title=f'POTENTIAL point={point}, i={i}, weight={potential_better_weight} (A)')
                print(f'Tour ({potential_better_weight}): {potential_better_tour}')

            if best_weight is None or best_weight > potential_better_weight:
                best_weight = potential_better_weight
                best_path_a = potential_better_a
                best_path_b = potential_better_b

        for i in range(len(path_b) + 1):
            potential_better_b, potential_better_a = insert_at_index_fast(path_b, path_a, i, point)
            potential_better_tour = paths_to_tour(potential_better_a, potential_better_b, points)
            potential_better_weight = tour_weight(potential_better_tour)
            if 'DEBUG' in environ:
                print(f'Potential Path A: {potential_better_a}')
                print(f'Potential Path B: {potential_better_b}')
                print_plottertour(potential_better_tour, MAX_VALUE, MAX_VALUE,
                                  path_a=[points[0]] + potential_better_a + [points[-1]],
                                  path_b=[points[0]] + potential_better_b + [points[-1]],
                                  title=f'POTENTIAL point={point}, i={i}, weight={potential_better_weight} (B)')
                print(f'Tour ({potential_better_weight}): {potential_better_tour}')
            if best_weight is None or best_weight > potential_better_weight:
                best_weight = potential_better_weight
                best_path_a = potential_better_a
                best_path_b = potential_better_b

        path_a = best_path_a
        path_b = best_path_b
        tour = paths_to_tour(path_a, path_b, points)
        if 'DEBUG' in environ:
            print_plottertour(tour, MAX_VALUE, MAX_VALUE,
                              path_a=[points[0]] + path_a + [points[-1]],
                              path_b=[points[0]] + path_b + [points[-1]],
                              title=f'FINAL point={point}')
            print()
            print(f'FINAL A: {path_a}')
            print(f'FINAL B: {path_b}')
            print()

    return [points[0]] + path_a + [points[-1]] + list(reversed(path_b)), path_a, path_b


def main() -> None:
    points = [(0,0), (1,6), (2,3), (3,5), (4,1), (5,1), (6,5), (7,4), (8,7), (9,3), (10,7), (11,7), (12,1)]
    points = list(map(lambda p: Point(p[0], p[1]), points))
    points = gen_points(MAX_VALUE, NUM_POINTS)
    # points = [Point(x=0, y=10), Point(x=2, y=1), Point(x=3, y=4), Point(x=4, y=10), Point(x=5, y=2), Point(x=6, y=4), Point(x=7, y=9), Point(x=8, y=3), Point(x=9, y=0), Point(x=10, y=5)]
    print(points)

    print()

    best_tour = optimal_tour(points)
    print(best_tour)
    print(tour_weight(best_tour))
    print_plottertour(best_tour, MAX_VALUE, MAX_VALUE, title='Result best')

    print()

    paths_tour, path_a, path_b = plottertour_paths(points)
    print(paths_tour)
    print(tour_weight(paths_tour))
    print_plottertour(paths_tour, MAX_VALUE, MAX_VALUE, title='Result paths')


def check_uniqueness() -> None:
    points = gen_points(MAX_VALUE - 5, NUM_POINTS - 5)
    opts = optimal_tours(points)
    if len(opts) == 2:
        if opts[0] == list(reversed(opts[1])):
            print('JUST THE REVERSE')
    for opt in opts:
        print(opt)
        print_plottertour(opt, MAX_VALUE, NUM_POINTS)


if __name__ == '__main__':

    main()
