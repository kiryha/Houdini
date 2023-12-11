"""
Procedural geometry
"""


def plane(rows, columns):
    """
    int[] faceVertexCounts =  [4]
    int[] faceVertexIndices = [0, 1, 2, 3]
    point3f[] points =        [(-5, 0, -5), (5, 0, -5), (5, 0, 5), (-5, 0, 5)]
    """

    points = []  # List of point positions
    face_vertex_counts = []  # List of vertex count per face
    face_vertex_indices = []  # List of vertex indices

    # Plane dimensions (corner coordinates)
    dimensions = [(-1, 0, 1), (1, 0, 1), (1, 0, -1), (-1, 0, -1)]

    face_number = 0
    for row in range(rows):
        for column in range(columns):
            print(f'prim number = {face_number}, r:{row}, c:{column}')

            # Add 4 points
            for point_number in range(0, 4):
                print(f'point {point_number}')
                points.append(dimensions[point_number])
                face_vertex_indices.append(point_number)

            face_vertex_counts.append(4)

            face_number += 1

    plane_data = {'points': points,
                  'face_vertex_counts': face_vertex_counts,
                  'face_vertex_indices': face_vertex_indices}

    return plane_data
