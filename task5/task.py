import json


def read_json(filename):
    with open(filename, encoding='UTF-8') as f:
        mass = json.load(f)
    return mass


def find_places(mass):
    a = {}
    for i, cluster in enumerate(mass):
        if isinstance(cluster, int):
            a[cluster] = i
        else:
            for elem in cluster:
                a[elem] = i
    return a


def find_place_and_trans(mass):
    a, trans = {}, {}
    length = 0
    for i, cluster in enumerate(mass):
        if isinstance(cluster, int):
            a[cluster] = i
            trans[length] = cluster
            length += 1
        else:
            for elem in cluster:
                a[elem] = i
                trans[length] = elem
                length += 1
    return a, trans


def create_table(mass, trans=None):
    if trans is not None:
        a = find_places(mass)
    else:
        a, trans = find_place_and_trans(mass)
    length = len(trans)

    table = [[0] * length for _ in range(length)]

    for i in range(length):
        for j in range(length):
            if a[trans[j]] <= a[trans[i]]:
                table[j][i] = 1

    return table, trans


def find_controversy(t1, t2, trans):
    t1_transpose = [list(i) for i in zip(*t1)]
    t2_transpose = [list(i) for i in zip(*t2)]

    t_mult = [[cell for cell in row] for row in t1]
    t_mult_transpose = [[cell for cell in row] for row in t1_transpose]
    kernel = [[0] * len(t1) for _ in range(len(t1))]
    zeros = set()

    for i in range(len(t1)):
        for j in range(len(t1)):
            t_mult[i][j] *= t2[i][j]
            t_mult_transpose[i][j] *= t2_transpose[i][j]
            kernel[i][j] = (t_mult[i][j] or t_mult_transpose[i][j])

            if not (kernel[i][j] or (j, i) in zeros):
                zeros.add((i, j))

    return merge_pairs([[trans[i], trans[j]] for i, j in zeros])


def merge_pairs(pair_array):
    merged_arrays = []

    for pair in pair_array:
        added = False

        for merged_array in merged_arrays:
            if any(element in merged_array for element in pair):
                merged_array.extend(pair)
                added = True
                break

        if not added:
            merged_arrays.append(list(pair))

    return [list(set(i)) for i in merged_arrays]


def make_experts_answer(controversy, trans):
    visited = set()
    answer = []

    for value in trans.values():
        if value not in visited:
            new_cluster = set()
            new_cluster.add(value)
            visited.add(value)

            for cluster in controversy:
                if value in cluster:
                    new_cluster.update(cluster)
                    visited.update(cluster)

            answer.append(list(new_cluster) if len(new_cluster) > 1 else new_cluster.pop())

    return answer



def task():
    a_data = read_json('ranj_b.json')
    b_data = read_json('ranj_a.json')

    a, trans = create_table(a_data)
    b, b_trans = create_table(b_data, trans)

    controversy = find_controversy(a, b, trans)
    answer = make_experts_answer(controversy, trans)
    return answer


if __name__ == '__main__':
    ans = task()
    print(ans)

