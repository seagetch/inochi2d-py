from ..api import *
from .node import *
import json


class InvalidCast(RuntimeError):
    def __init__(self, obj):
        super(InvalidCast, self).__init__("src must be Node object, but get object of type %s"%type(obj))

class MeshData:
    def __init__(self, verts, uvs, indices, axes, origin):
        self.verts   = verts
        self.uvs     = uvs
        self.indices = indices
        self.axes    = axes
        self.origin  = origin

class Drawable(Node):
    def __init__(self, src):
        if isinstance(src, Node):
            self.handle = src.handle
        else:
            raise InvalidCast(src)
        
    def __del__(self):
        pass

    @classmethod
    def set_update_bounds(self, value):
        inSetUpdateBounds(value)

    @property
    def vertices(self):
        return inDrawableGetVertices(self.handle)
    
    @vertices.setter
    def vertices(self, value):
        inDrawableSetVertices(self.handle, value)

    @property
    def deformation(self):
        return inDrawableGetDeformation(self.handle)

    def refresh(self):
        inDrawableRefresh(self.handle)

    def refresh_deform(self):
        inDrawableRefreshDeform(self.handle)

    def reset(self):
        inDrawableReset(self.handle)

    def draw_bounds(self):
        inDrawableDrawBounds(self.handle)

    def draw_mesh_lines(self):
        inDrawableDrawMeshLines(self.handle)

    def draw_mesh_points(self):
        inDrawableDrawMeshPoints(self.handle)

    @property
    def dynamic_matrix(self):
        return inDrawableGetDynamicMatrix(self.handle)

    @property
    def mesh(self):
        return MeshData(*inDrawableGetMeshData(self.handle))
    
    @mesh.setter
    def mesh(self, mesh):
        inDrawableSetMeshData(self.handle, mesh.verts, mesh.uvs, mesh.indices, mesh.axes, mesh.origin)