from utils import *
from typing import Tuple
from os import environ


NUM_POINTS = 10
MAX_VALUE = 15


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
            potential_better_a, potential_better_b = insert_at_index(path_a, path_b, i, point)
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
            potential_better_b, potential_better_a = insert_at_index(path_b, path_a, i, point)
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
    points = gen_points(MAX_VALUE, NUM_POINTS)
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


if __name__ == '__main__':
    main()
