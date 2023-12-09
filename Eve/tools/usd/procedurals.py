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

    face_number = 0
    for row in range(rows):
        for column in range(columns):

            print(f'prim number = {face_number}')

            face_number += 1

    plane_data = {'points': points,
                  'face_vertex_counts': face_vertex_counts,
                  'face_vertex_indices': face_vertex_indices}

    return plane_data


plane(1, 1)
