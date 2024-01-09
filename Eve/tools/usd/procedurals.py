"""
Write procedural geometry to USD file

USD plane:
int[] faceVertexCounts =  [4]
int[] faceVertexIndices = [0, 1, 2, 3]
point3f[] points =        [(-5, 0, -5), (5, 0, -5), (5, 0, 5), (-5, 0, 5)]
"""


import math
import copy


# Geometry manipulation classes
class MeshData:
    """
    Geometry container: define points, polygons etc

    self.points: List of point positions
    self.face_vertex_counts: List of vertex count per face (each element is a face)
    self.face_vertex_indices: List of vertex indices
    """

    def __init__(self):

        self.points = []
        self.face_vertex_counts = []
        self.face_vertex_indices = []

    def add_point(self, point):
        """
        Add a single point to the mesh.
        """
        self.points.append(point)

    def add_points(self, points):
        """
        Add list of points to the mesh.
        """
        self.points.extend(points)

    def add_face(self, face_vertex_counts, face_vertex_indices):
        """
        Add a single face to the mesh.
        """

        self.face_vertex_counts.append(face_vertex_counts)
        self.face_vertex_indices.extend(face_vertex_indices)


class EditMesh:
    """
    Geometry manipulation: edit geometry container data
    """

    def __init__(self, mesh_data):
        self.source_mesh = mesh_data
        self.modified_mesh = copy.deepcopy(mesh_data)

    def extrude_face(self, extrude_distance):
        """
        Extrude a single 4 points XZ polygon
        """

        # Loop face points and extend points with new extruded points
        for point in self.source_mesh.points:
            extruded_point = (point[0], point[1] + extrude_distance, point[2])
            self.modified_mesh.add_point(extruded_point)

        # Add face for each pair of old/new points (edges)
        source_points = len(self.source_mesh.points)
        for index in range(source_points):
            lower_left = index
            lower_right = (index + 1) % source_points
            upper_right = ((index + 1) % source_points) + source_points
            upper_left = index + source_points

            quad = [upper_left, upper_right, lower_right, lower_left]
            self.modified_mesh.add_face(4, quad)

        # Add top face
        # self.modified_mesh.add_face(4, [7, 6, 5, 4])
        top_face_indices = []
        for i in range(source_points, 2 * source_points):
            top_face_indices.append(i)

        self.modified_mesh.add_face(4, top_face_indices[::-1])

        return self.modified_mesh


# Math
def get_cartesian_position(h_angle, v_angle):
    """
    Convert polar to cartesian coordinates
    """

    position = (math.sin(v_angle) * math.cos(h_angle), math.cos(v_angle), math.sin(v_angle) * math.sin(h_angle))

    return position


# Procedural shapes
def polygon(points=None):
    """
    Create single polygon from input list of point positions
    If points are not provided, create a unit plane.
    """

    if points is None:
        points = [(-1, 0, 1), (1, 0, 1), (1, 0, -1), (-1, 0, -1)]

    mesh_data = MeshData()
    mesh_data.add_points(points)
    mesh_data.add_face(len(points), [i for i in range(len(points))])

    return mesh_data


def plane(row_points, column_points):
    """
    Create polygonal grid
    """

    mesh_data = MeshData()

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
            mesh_data.add_point((x, 0, z))

    # Define faces using the indices of the grid points
    for row_point in range(row_points - 1):
        for column_point in range(column_points - 1):
            # Calculate the indices of the corners of the cell
            top_left = row_point * column_points + column_point
            top_right = top_left + 1
            bottom_left = top_left + column_points
            bottom_right = bottom_left + 1

            # Define the face using the indices of the 4 corners
            mesh_data.add_face(4, [top_left, top_right, bottom_right, bottom_left])

    return mesh_data


def sphere(h_points, v_points):
    """
    Create polygonal sphere
    """

    mesh_data = MeshData()

    # Crate sphere points
    # Top pole
    top_pole_position = get_cartesian_position(0, 0)
    mesh_data.add_point(top_pole_position)

    for v_point in range(1, v_points - 1):  # Range excludes poles
        v_angle = v_point * 3.14 / (v_points - 1)

        for h_point in range(h_points):
            h_angle = 2 * h_point * 3.14 / h_points

            position = get_cartesian_position(h_angle, v_angle)
            mesh_data.add_point(position)

    # Bottom pole
    bottom_pole_position = get_cartesian_position(0, 3.142)
    mesh_data.add_point(bottom_pole_position)

    # Create sphere faces
    # Top pole faces
    top_pole_index = 0
    first_row_start = 1
    for h_point in range(h_points):
        next_point = (h_point + 1) % h_points
        mesh_data.add_face(3, [top_pole_index, first_row_start + h_point, first_row_start + next_point])

    # Main body faces (quads)
    for v_point in range(1, v_points - 2):
        row_start = 1 + (v_point - 1) * h_points
        next_row_start = row_start + h_points
        for h_point in range(h_points):
            next_point = (h_point + 1) % h_points
            mesh_data.add_face(4, [next_row_start + h_point, next_row_start + next_point, row_start + next_point, row_start + h_point])

    # Bottom pole faces
    bottom_pole_index = len(mesh_data.points) - 1
    last_row_start = 1 + (v_points - 3) * h_points
    for h_point in range(h_points):
        next_point = (h_point + 1) % h_points
        mesh_data.add_face(3, [bottom_pole_index, last_row_start + next_point, last_row_start + h_point])

    return mesh_data


def torus(h_points, v_points, radius, thickness):
    """
    Create poly donut
    """

    mesh_data = MeshData()

    # Create torus points
    for h_point in range(h_points):
        for v_point in range(v_points):
            u = (v_point * 2 * math.pi) / v_points  # Angle around the ring
            v = (h_point * 2 * math.pi) / h_points  # Angle around the tube

            x = (radius + thickness * math.cos(v)) * math.cos(u)
            y = (radius + thickness * math.cos(v)) * math.sin(u)
            z = thickness * math.sin(v)

            position = (x, y, z)
            mesh_data.add_point(position)

    # Create torus faces
    for h_point in range(h_points):
        h_next = (h_point + 1) % h_points
        for v_point in range(v_points):
            v_next = (v_point + 1) % v_points

            top_left = h_point * v_points + v_point
            top_right = h_point * v_points + v_next
            bottom_left = h_next * v_points + v_next
            bottom_right = h_next * v_points + v_point

            mesh_data.add_face(4, [top_left, top_right, bottom_left, bottom_right])

    return mesh_data


def cone(resolution):
    """
    Create poly cone
    """

    mesh_data = MeshData()

    # Create cone points
    for point in range(resolution):
        angle = 2.0 * 3.14 * point / resolution
        x = math.cos(angle)
        z = math.sin(angle)
        mesh_data.add_point((x, 0, z))

    # Add tip
    mesh_data.add_point((0, 2, 0))

    # Crete cone faces
    for point in range(resolution):
        triangle = [point, point + 1, resolution]
        mesh_data.add_face(3, triangle)

    # Bottom face
    mesh_data.add_face(resolution, [i for i in range(resolution)])

    return mesh_data
