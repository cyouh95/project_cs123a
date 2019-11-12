import json
import csv


def get_min_distance(m):
    min_dist = float('inf')
    min_i, min_j = None, None

    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] < min_dist:
                min_dist = m[i][j]
                min_i, min_j = i, j

    return min_i, min_j


def regenerate_matrix(m, d):
    x, y = get_min_distance(m)
    dist = m[x][y] / 2

    old_idx = [idx for idx in range(len(d)) if idx not in (x, y)]
    children = [entry for idx, entry in enumerate(d) if idx in (x, y)]

    new_name = d[x]['name'] + '|' + d[y]['name']
    new_row = []

    for idx in old_idx:
        x_dist = m[x][idx] if idx < x else m[idx][x]
        y_dist = m[y][idx] if idx < y else m[idx][y]

        avg_dist = (x_dist + y_dist) / 2
        new_row.append(avg_dist)

    d = [entry for idx, entry in enumerate(d) if idx in old_idx]
    m = [[d for i, d in enumerate(row) if i in old_idx] for idx, row in enumerate(m) if idx in old_idx]

    d.append({'name': new_name, 'distance': dist, 'children': children})
    m.append(new_row)

    return m, d


def get_json(file, tab=False):
    if tab:
        reader = csv.reader(file.splitlines(), delimiter='\t')
    else:
        reader = csv.reader(file)

    data = []
    matrix = []

    for idx, row in enumerate(reader):
        data.append({'name': row.pop(0), 'distance': 0})
        matrix.append([float(i) for i in row[:idx]])

    while len(data) > 1:
        matrix, data = regenerate_matrix(matrix, data)

    return json.dumps(data[0])
