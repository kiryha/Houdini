"""
Write procedural geometry to USD file

USD plane:
int[] faceVertexCounts =  [4]
int[] faceVertexIndices = [0, 1, 2, 3]
point3f[] points =        [(-5, 0, -5), (5, 0, -5), (5, 0, 5), (-5, 0, 5)]
"""


import math
import copy
import numpy as np


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

    def add_face(self, face_vertex_counts, face_vertex_indices):
        """
        Add a single face to the mesh.
        """

        self.face_vertex_counts.append(face_vertex_counts)
        self.face_vertex_indices.extend(face_vertex_indices)

    def get_face(self, face_number):
        """
        Get and return data for current face
        """

        face_data = MeshData()

        # Get the indices of the vertices that make up the face
        start = sum(self.face_vertex_counts[:face_number])
        end = start + self.face_vertex_counts[face_number]
        vertex_indices = self.face_vertex_indices[start:end]

        # Get point positions
        for index in vertex_indices:
            face_data.add_point(self.points[index])

        # Record face data
        face_data.add_face(len(vertex_indices), vertex_indices)

        return face_data

    def get_normal(self, face_data):
        """
        Calculate normal of a face
        """

        # Get first 3 points from face
        point_1 = np.array(face_data.points[0])
        point_2 = np.array(face_data.points[1])
        point_3 = np.array(face_data.points[2])

        # Calculate the normalized normal as a list
        normal = np.cross(point_2 - point_1, point_3 - point_1)
        normal = normal / np.linalg.norm(normal)
        normal = normal.tolist()

        return normal


class EditMesh:
    """
    Geometry manipulation: edit geometry container data
    """

    def __init__(self, mesh_data):
        self.source_mesh = mesh_data
        self.modified_mesh = copy.deepcopy(mesh_data)

    def shift_point(self, point, vector, length):
        """
        Move point along vector, return new point coordinates as a list
        """

        point = np.array(point)
        vector = np.array(vector)
        shifted_point = point + vector * length
        shifted_point = shifted_point.tolist()

        return shifted_point

    def extrude_face(self, face_number, extrude_distance):
        """
        Extrude polygon along normal
        """

        # Get selected face data
        face_data = self.source_mesh.get_face(face_number)
        face_normal = face_data.get_normal(face_data)
        number_of_points_source = len(self.modified_mesh.points)
        polygon_points_number = len(face_data.points)

        # Loop face points and extend points with new extruded points
        for point in face_data.points:
            extruded_point = self.shift_point(point, face_normal, extrude_distance)
            self.modified_mesh.add_point(extruded_point)

        # Add face for each pair of old/new points (edges)
        for index in range(polygon_points_number):
            global_index = face_data.face_vertex_indices[index]
            next_global_index = face_data.face_vertex_indices[(index + 1) % polygon_points_number]

            lower_left = global_index
            lower_right = next_global_index
            upper_left = number_of_points_source + index
            upper_right = number_of_points_source + (index + 1) % polygon_points_number

            quad = [lower_left, lower_right, upper_right, upper_left]
            self.modified_mesh.add_face(4, quad)

        # Add top face to close the extrusion
        top_face_indices = []
        for i in range(number_of_points_source, number_of_points_source + polygon_points_number):
            top_face_indices.append(i)

        self.modified_mesh.add_face(polygon_points_number, top_face_indices)

        # TODO! Delete source face

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

    # Add points
    for point in points:
        mesh_data.add_point(point)

    # Add faces
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
