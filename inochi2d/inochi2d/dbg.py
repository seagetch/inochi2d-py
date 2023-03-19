
from ..api import *

class Dbg:
    @property
    def draw_mesh_outlines(module):
        return inGetDbgDrawMeshOutlines()
    @draw_mesh_outlines.setter
    def draw_mesh_outlines(module, value):
        inSetDbgDrawMeshOutlines(value)

    @property
    def draw_mesh_vertex_points(module):
        return inGetDbgDrawMeshVertexPoints()

    @draw_mesh_vertex_points.setter
    def draw_mesh_vertex_points(module, value):
        inSetDbgDrawMeshVertexPoints(value)

    @property
    def draw_mesh_orientation(module):
        return inGetDbgDrawMeshOrientation()
    @draw_mesh_orientation.setter
    def draw_mesh_orientation(module, value):
        return inSetDbgDrawMeshOrientation(value)

    def points_size(module, size):
        inDbgPointsSize(size)

    def line_width(module, width):
        inDbgLineWidth(width)

    def set_buffer(module, points, indices = None):
        if indices is None:
            inDbgSetBuffer(points)
        else:
            inDbgSetBufferWithIndices(points, indices)

    def draw_points(module, color, matrix):
        inDbgDrawPoints(color, matrix)

    def draw_lines(module, color, matrix):
        inDbgDrawLines(color, matrix)

dbg = Dbg()