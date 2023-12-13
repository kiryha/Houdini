"""
Procedural geometry
"""
import math


def get_cartesian_position(h_angle, v_angle):

    position = [math.sin(v_angle) * math.cos(h_angle), math.sin(v_angle) * math.sin(h_angle), math.cos(v_angle)]

    return position


def plane(row_points, column_points):
    """
    Create polygonal grid (size 2x2 units)

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
    row_spacing = height / (row_points - 1)
    col_spacing = width / (column_points - 1)

    # Generate points for the grid
    for row_point in range(row_points):
        for column_point in range(column_points):
            x = column_point * col_spacing - width / 2
            z = row_point * row_spacing - height / 2
            points.append((x, 0, z))

    # Define faces using the indices of the grid points
    for row_point in range(row_points - 1):
        for column_point in range(column_points - 1):
            # Calculate the indices of the corners of the cell
            top_left = row_point * column_points + column_point
            top_right = top_left + 1
            bottom_left = top_left + column_points
            bottom_right = bottom_left + 1

            # Define the face using the indices of the 4 corners
            face_vertex_indices.extend([top_left, top_right, bottom_right, bottom_left])
            face_vertex_counts.append(4)

    geometry_data = {'points': points,
                     'face_vertex_counts': face_vertex_counts,
                     'face_vertex_indices': face_vertex_indices}

    return geometry_data


def sphere(h_points, v_points):
    """
    Create polygonal sphere
    """

    points = []  # List of point positions
    face_vertex_counts = []  # List of vertex count per face
    face_vertex_indices = []  # List of vertex indices

    # Crate sphere points
    for v_point in range(v_points):
        v_angle = v_point * (3.14 / v_points)

        # Handle poles
        if v_point == 0 or v_point == v_points-1:
            continue

        for h_point in range(h_points):
            h_angle = h_point * (2 * 3.14 / h_points)
            position = get_cartesian_position(h_angle, v_angle)

    geometry_data = {'points': points,
                     'face_vertex_counts': face_vertex_counts,
                     'face_vertex_indices': face_vertex_indices}

    return geometry_data
