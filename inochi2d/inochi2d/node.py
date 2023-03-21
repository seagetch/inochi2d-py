from ..api import *
import json

class Node:
    def __init__(self, handle):
        self.handle = handle

    def __del__(self):
        inNodeDestroy(self.handle)
        self.handle = None

    @property
    def name(self):
        return inNodeGetName(self.handle)
    
    @property
    def uuid(self):
        return inNodeGetUUID(self.handle)
    
    @property
    def type_id(self):
        return inNodeGetTypeId(self.handle)

    @property
    def enabled(self):
        return inNodeGetEnabled(self.handle)

    @property
    def path(self):
        return inNodeGetPath(self.handle)
        
    def lock_to_root(self):
        return inNodeGetLockToRoot(self.handle)
    
    def draw(self):
        return inNodeDraw(self.handle)
    
    def draw_one(self):
        return inNodeDrawOne(self.handle)
    
    def update(self):
        return inNodeUpdate(self.handle)
    
    def begin_update(self):
        return inNodeBeginUpdate(self.handle)
    
    def transform_changed(self):
        return inNodeTransformChanged(self.handle)

    def children(self):
        children = inNodeGetChildren(self.handle)
        return [Node(handle) for handle in children]
    
    def loads(self, data):
        text = json.dumps(data)
        inNodeLoadJson(self.handle, text)

    def dumps(self, recursive = True):
        text = inNodeDumpJson(self.handle, recursive)
        return json.loads(text)
    
    @property
    def transform(self):
        return inNodeGetTransformMatrix(self.handle)
    
    @property
    def local_transform(self):
        return inNodeGetLocalTransformMatrix(self.handle)
    
    def get_value(self, name):
        return inNodeGetValue(self.handle, name)
    
    def set_value(self, name, value):
        inNodeSetValue(self.handle, name, value)

    @property
    def translation(self):
        return inNodeGetTranslation(self.handle)

    @translation.setter
    def translation(self, value):
        if isinstance(value, np.ndarray):
            value = value.tolist()
        return inNodeSetTranslation(self.handle, *value)

    @property
    def rotation(self):
        return inNodeGetRotation(self.handle)

    @rotation.setter
    def rotation(self, value):
        if isinstance(value, np.ndarray):
            value = value.tolist()
        return inNodeSetRotation(self.handle, *value)

    @property
    def scale(self):
        return inNodeGetScale(self.handle)

    @scale.setter
    def scale(self, value):
        if isinstance(value, np.ndarray):
            value = value.tolist()
        return inNodeSetScale(self.handle, *value)
    
    @property
    def combined_bounds(self):
        return inNodeGetCombinedBounds(self.handle)