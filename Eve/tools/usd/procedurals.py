"""
Write procedural geometry to USD file

USD plane:
int[] faceVertexCounts =  [4]
int[] faceVertexIndices = [0, 1, 2, 3]
point3f[] points =        [(-5, 0, -5), (5, 0, -5), (5, 0, 5), (-5, 0, 5)]
"""


import math


def get_cartesian_position(h_angle, v_angle):
    """
    Convert polar to cartesian coordinates
    """

    position = (math.sin(v_angle) * math.cos(h_angle), math.cos(v_angle), math.sin(v_angle) * math.sin(h_angle))

    return position


def plane(row_points, column_points):
    """
    Create polygonal grid
    """

    points = []  # List of point positions
    face_vertex_counts = []  # List of vertex count per face
    face_vertex_indices = []  # List of vertex indices

    # Spacing between points
    width = 1
    height = 1
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
    # Top pole
    top_pole_position = get_cartesian_position(0, 0)
    points.append(top_pole_position)

    for v_point in range(1, v_points - 1):  # Range excludes poles
        v_angle = v_point * 3.14 / (v_points - 1)

        for h_point in range(h_points):
            h_angle = 2 * h_point * 3.14 / h_points

            position = get_cartesian_position(h_angle, v_angle)
            points.append(position)

    # Bottom pole
    bottom_pole_position = get_cartesian_position(0, 3.142)
    points.append(bottom_pole_position)

    # Create sphere faces
    # Top pole faces
    top_pole_index = 0
    first_row_start = 1
    for h_point in range(h_points):
        next_point = (h_point + 1) % h_points
        face_vertex_indices.extend([top_pole_index, first_row_start + h_point, first_row_start + next_point])
        face_vertex_counts.append(3)

    # Main body faces (quads)
    for v_point in range(1, v_points - 2):
        row_start = 1 + (v_point - 1) * h_points
        next_row_start = row_start + h_points
        for h_point in range(h_points):
            next_point = (h_point + 1) % h_points
            face_vertex_indices.extend([next_row_start + h_point, next_row_start + next_point, row_start + next_point, row_start + h_point])
            face_vertex_counts.append(4)

    # Bottom pole faces
    bottom_pole_index = len(points) - 1
    last_row_start = 1 + (v_points - 3) * h_points
    for h_point in range(h_points):
        next_point = (h_point + 1) % h_points
        face_vertex_indices.extend([bottom_pole_index, last_row_start + next_point, last_row_start + h_point])
        face_vertex_counts.append(3)

    geometry_data = {'points': points,
                     'face_vertex_counts': face_vertex_counts,
                     'face_vertex_indices': face_vertex_indices}

    return geometry_data


def torus(h_points, v_points, radius, thickness):
    """
    Create poly donut
    """

    points = []  # List of point positions
    face_vertex_counts = []  # List of vertex count per face
    face_vertex_indices = []  # List of vertex indices

    # Create torus points
    for h_point in range(h_points):
        for v_point in range(v_points):
            u = (v_point * 2 * math.pi) / v_points  # Angle around the ring
            v = (h_point * 2 * math.pi) / h_points  # Angle around the tube

            x = (radius + thickness * math.cos(v)) * math.cos(u)
            y = (radius + thickness * math.cos(v)) * math.sin(u)
            z = thickness * math.sin(v)

            position = (x, y, z)
            points.append(position)

    # Create torus faces
    for h_point in range(h_points):
        h_next = (h_point + 1) % h_points
        for v_point in range(v_points):
            v_next = (v_point + 1) % v_points

            top_left = h_point * v_points + v_point
            top_right = h_point * v_points + v_next
            bottom_left = h_next * v_points + v_next
            bottom_right = h_next * v_points + v_point

            face_vertex_indices.extend([top_left, top_right, bottom_left, bottom_right])
            face_vertex_counts.append(4)

    geometry_data = {'points': points,
                     'face_vertex_counts': face_vertex_counts,
                     'face_vertex_indices': face_vertex_indices}

    return geometry_data


def cone(resolution):
    """
    Create poly cone
    """

    points = []  # List of point positions
    face_vertex_counts = []  # List of vertex count per face
    face_vertex_indices = []  # List of vertex indices

    # Create cone points
    for point in range(resolution):
        angle = 2.0 * 3.14 * point / resolution

        x = math.cos(angle)
        z = math.sin(angle)
        points.append((x, 0, z))

    # Add tip
    points.append((0, 2, 0))

    # Crete cone faces
    for point in range(resolution):
        triangle = [point, point + 1, resolution]
        face_vertex_indices.extend(triangle)
        face_vertex_counts.append(3)

    # Bottom face
    for point in range(resolution):
        face_vertex_indices.append(point)
    face_vertex_counts.append(resolution)

    geometry_data = {'points': points,
                     'face_vertex_counts': face_vertex_counts,
                     'face_vertex_indices': face_vertex_indices}

    return geometry_data
