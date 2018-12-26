import re


def point_in_cluster(point, cluster):
    for p in cluster:
        dist = 0
        for i in range(4):
            dist += abs(p[i] - point[i])
        if dist <= 3:
            return True

    return False


def cluster_points(filename):
    clusters = []

    for line in open(filename, 'r').readlines():
        point = tuple((int(d) for d in re.findall(r'-?\d+', line)))

        matching_clusters = []
        for idx, cluster in enumerate(clusters):
            if point_in_cluster(point, cluster):
                matching_clusters.append(idx)

        # No clusters, so we create a new one
        if len(matching_clusters) == 0:
            clusters.append({point})

        # Part of 1 cluster, add it
        elif len(matching_clusters) == 1:
            clusters[matching_clusters[0]].add(point)

        # Merge clusters
        else:
            # Merge all clusters here
            base_idx = matching_clusters[0]

            # Reverse iterate to prevent deleting issues
            for idx in reversed(matching_clusters[1:]):
                clusters[base_idx] = clusters[base_idx].union(clusters[idx])
                del clusters[idx]

            clusters[base_idx].add(point)

    return clusters


def spacetime():
    clusters = cluster_points('input.txt')
    print('The points form {} constellation(s).'.format(len(clusters)))


spacetime()
