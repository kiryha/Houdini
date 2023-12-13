"""
Procedural geometry
"""
import math


def get_cartesian_position(h_angle, v_angle):
    """
    Convert polar to cartesian coordinates
    """

    position = (math.sin(v_angle) * math.cos(h_angle), math.sin(v_angle) * math.sin(h_angle), math.cos(v_angle))

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
    points.append((0, 0, 1))  # Top pole

    for v_point in range(1, v_points - 1):  # Range excludes poles
        v_angle = v_point * 3.14 / (v_points - 1)

        for h_point in range(h_points):
            h_angle = 2 * h_point * 3.14 / h_points

            position = get_cartesian_position(h_angle, v_angle)
            points.append(position)

    points.append((0, 0, -1))  # Bottom pole

    # Create sphere faces
    # Main body faces (quads)
    for v_point in range(1, v_points - 2):
        row_start = 1 + (v_point - 1) * h_points
        next_row_start = row_start + h_points
        for h_point in range(h_points):
            next_point = (h_point + 1) % h_points
            face_vertex_indices.extend([row_start + h_point,
                                        row_start + next_point,
                                        next_row_start + next_point,
                                        next_row_start + h_point])
            face_vertex_counts.append(4)

    geometry_data = {'points': points,
                     'face_vertex_counts': face_vertex_counts,
                     'face_vertex_indices': face_vertex_indices}

    return geometry_data
