from typing import TypeAlias

import pandas


Matrix: TypeAlias = dict[int, dict[int, int]]
Ranges: TypeAlias = list[int]


left_border = 1
right_border = 10


def is_belong(item: tuple[int, int]) -> bool:
    a, b = item
    return 3 * a <= 5 * b


def is_reflexively(ranges: Ranges) -> bool:
    for a in ranges:
        if not is_belong((a, a)):
            return False
    return True


def is_anti_reflexively(ranges: Ranges) -> bool:
    for a in ranges:
        if is_belong((a, a)):
            return False
    return True


def is_symmetrically(ranges: Ranges) -> bool:
    for a in ranges:
        for b in ranges:
            if is_belong((a, b)) != is_belong((b, a)):
                return False
    return True


def is_anti_symmetrically(ranges: Ranges) -> bool:
    for a in ranges:
        for b in ranges:
            if is_belong((a, b)) * is_belong((b, a)) != 0:
                return False
    return True


def is_transitively(ranges: Ranges) -> bool:
    for a in ranges:
        for b in ranges:
            for c in ranges:
                if is_belong((a, b)) \
                        and is_belong((b, c)) \
                        and not is_belong((a, c)):
                    return False
    return True


def is_equivalence(ranges: Ranges) -> bool:
    return is_reflexively(ranges) \
            and is_symmetrically(ranges) \
            and is_transitively(ranges)


def get_composition(r1: Matrix, r2: Matrix, ranges: Ranges) -> Matrix:
    matrix = {i: {j: 0 for j in ranges} for i in ranges}
    for a in ranges:
        for b in ranges:
            for c in ranges:
                if not matrix[a][b]:
                    matrix[a][b] = r1[a][c] * r2[c][b]
    return matrix


def get_matrix(ranges: Ranges) -> Matrix:
    matrix = {i: {j: 0 for j in ranges} for i in ranges}
    for a in ranges:
        for b in ranges:
            matrix[a][b] = int(is_belong((a, b)))

    return matrix


def get_short_curcuit(matrix: Matrix, ranges: Ranges) -> Matrix:
    result = {i: {j: 0 for j in ranges} for i in ranges}
    last = matrix
    i = 1
    compositions: list[tuple[Matrix, int]] = [(matrix, i)]
    while True:
        composition = get_composition(last, matrix, ranges)
        if composition == last:
            break
        last = composition
        i += 1
        compositions.append((last, i))

    for i in ranges:
        for j in ranges:
            for comp, _ in compositions:
                result[i][j] = result[i][j] or comp[i][j]

    for comp, i in compositions:
        print('\nComposition:', i)
        print_matrix(comp)
    print()

    return result


def print_matrix(matrix: Matrix) -> None:
    print(pandas.DataFrame.from_dict(matrix, orient='index'))


def main() -> None:
    ranges = list(range(left_border, right_border + 1))
    print('Reflexively:', is_reflexively(ranges))
    print('Anti-reflexively:', is_anti_reflexively(ranges))
    print('Symmetrically:', is_symmetrically(ranges))
    print('Anti-Symmetrically:', is_anti_symmetrically(ranges))
    print('Transitively:', is_transitively(ranges))
    print('Equivalence:', is_equivalence(ranges))

    data = get_matrix(ranges)
    short_curcuit = get_short_curcuit(data, ranges)
    print('Transitively short curcuit')
    print_matrix(short_curcuit)


if __name__ == '__main__':
    main()
