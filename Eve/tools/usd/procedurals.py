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

    # Spacing between points
    width = 2
    height = 2
    row_spacing = height / rows
    col_spacing = width / columns

    point_index = 0
    for row in range(rows):
        for column in range(columns):

            # Calculate the corner positions of the current cell
            x0 = column * col_spacing - width / 2
            x1 = x0 + col_spacing
            z0 = row * row_spacing - height / 2
            z1 = z0 + row_spacing

            # Define the 4 corners of the cell
            points.append((x0, 0, z0))
            points.append((x1, 0, z0))
            points.append((x1, 0, z1))
            points.append((x0, 0, z1))

            # Define the face using the indices of the 4 corners
            face_vertex_indices.extend([point_index, point_index + 1, point_index + 2, point_index + 3])
            face_vertex_counts.append(4)
            point_index += 4

    plane_data = {'points': points,
                  'face_vertex_counts': face_vertex_counts,
                  'face_vertex_indices': face_vertex_indices}

    print(plane_data)
    return plane_data
