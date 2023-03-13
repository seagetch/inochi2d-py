from ..api import *

class Node:
    def __init__(self, handle):
        self.handle = handle

    def __del__(self):
        inNodeDestroy(self.handle)
        self.handle = None

    def name(self):
        return inNodeGetName(self.handle)
    
    def uuid(self):
        return inNodeGetUUID(self.handle)
    
    def type_id(self):
        return inNodeGetTypeId(self.handle)

    def enabled(self):
        return inNodeGetEnabled(self.handle)

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
    
    def loads(self, text):
        inNodeLoadJson(self.handle, text)

    def dumps(self):
        return inNodeDumpJson(self.handle)