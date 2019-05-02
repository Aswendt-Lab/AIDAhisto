import math

def closest_pair_2D(t):
    '''Function closest_pair_2D() returns the indices of the closest pair of points of a two-dimensional associative array.'''

    def sort_i_x_2D(t):
        return [i for (i,u) in sorted(enumerate(t), key = lambda p: p[1][0])]

    def sort_i_y_2D(t):
        return [i for (i,u) in sorted(enumerate(t), key = lambda p: p[1][1])]

    i_x = sort_i_x_2D(t)
    i_y = sort_i_y_2D(t)

    def distance(u,v):
        dx = u[0] - v[0]
        dy = u[1] - v[1]
        return dx*dx + dy*dy

    def search(i,j):
        if i >= j:
            return None
        elif i + 1 == j:
            return (i_x[i], i_x[j])
        else:
            k = (i + j) // 2
            left = search(i, k)
            right = search(k+1, j)

            if left is None:
                (i_min, j_min) = right
            elif right is None:
                (i_min, j_min) = left
            else:
                (i_left, j_left) = left
                (i_right, j_right) = right
                d_left = distance(t[i_left], t[j_left])
                d_right = distance(t[i_right], t[j_right])
                if d_left < d_right:
                    (i_min, j_min) = (i_left, j_left)
                else:
                    (i_min, j_min) = (i_right, j_right)

            d = distance(t[i_min], t[j_min])

            x = (t[i_x[k]][0] + t[i_x[k + 1]][0]) / 2

            area = [j for j in i_y if abs(t[j][0] - x) <= d]

            for p in range(len(area)):
                r = p + 1
                while r < len(area) and (t[i_y[r]][1] - t[i_y[p]][1]) < d and r - p <= 6:
                    e = distance(t[i_y[p]], t[i_y[r]])
                    if e < d:
                        d = e
                        i_min = p
                        j_min = r
                    r = r + 1
            return (i_min, j_min)

    return search(0, len(t) - 1)

print(closest_pair_2D([]))
# Function closest_pair_2D([]) returns: None.

print (closest_pair_2D([(1, 2)]))
# Function closest_pair_2D([(1, 2)]) returns: None.

print(closest_pair_2D([(1, 2), (3, 4)]))
# Function closest_pair_2D([(1, 2), (3, 4)]) returns (0, 1).

print(closest_pair_2D([(1, 2), (3, 4), (10, 20)]))
# Function closest_pair_2D([(1, 2), (3, 4), (10, 20)]) returns (0, 1).

print(closest_pair_2D([(1,2),(2,5),(4,2),(5,7),(6,4),(7,4),(9,7),(9,3),(9,1)]))
# Function closest_pair_2D([(1,2),(2,5),(4,2),(5,7),(6,4),(7,4),(9,7),(9,3),(9,1)]) returns (4, 5).

print(closest_pair_2D([(1,3),(8,2),(2,5),(9,5),(7,7)]))
# Function closest_pair_2D([(1,3),(8,2),(2,5),(9,5),(7,7)]) returns (0, 2).

print(closest_pair_2D([(-1000, -10), (-729, -9), (-512, -8), (-343, -7), (-216, -6), (-125, -5), (-64, -4), (-27, -3), (-8, -2), (-1, -1), (0, 0), (8, 2), (27, 3), (64, 4), (125, 5), (216, 6), (343, 7), (512, 8), (729, 9)]))
# Function closest_pair_2D([(-1000, -10), (-729, -9), (-512, -8), (-343, -7), (-216, -6), (-125, -5), (-64, -4), (-27, -3), (-8, -2), (-1, -1), (0, 0), (8, 2), (27, 3), (64, 4), (125, 5), (216, 6), (343, 7), (512, 8), (729, 9)]) returns (9, 10).
