def _resources(puppet, resources, res_type, klass, name=None, uuid=None):
    if resources is None:
        return None
    if name is None and uuid is None:
        return [klass().from_json(puppet, node) for node in resources]
    elif name is not None:
        return [klass().from_json(puppet, node) for node in resources if isinstance(node, dict) and name in node.get("name")]
    elif uuid is not None:
        return [klass().from_json(puppet, node) for node in resources if isinstance(node, dict) and node.get("uuid") == uuid]
    return None


class PuppetData:
    def __init__(self, puppet_json, textures, exts):
        self.textures    = textures
        self.exts        = exts
        self.root        = puppet_json
        
        self._nodes = []
        def collect_nodes(node):
            if not isinstance(node, dict):
                return
            self._nodes.append(node)
            if node.get("children"):
                for child in node.get("children"):
                    collect_nodes(child)
        collect_nodes(self.root.get("nodes"))
    
    def nodes(self, name=None, uuid=None):
        return _resources(self, self._nodes, "nodes", NodeData, name, uuid)
    
    def add_node(self, parent, node):

        # Updating json information
        new_puppet = self
        old_puppet = self
        
        if isinstance(parent, NodeData):
            new_pupppet = parent.puppet
            parent = parent.root
        if isinstance(node, NodeData):
            old_puppet = node.puppet
            node = node.root
        if parent.get("children") is None:
            parent["children"] = []
        parent.get("children").append(node)
        
        # Updating _nodes
        new_puppet._nodes.append(node)
        
        # Validating uniqueness of the uuid
        # Updating UUID, and maintain links if needed.

        # Updating texture slot
        if new_puppet != old_puppet:
            index = len(new_puppet.textures)
            node_textures = node.get("textures")
            if node_textures:
                for i, tex in enumerate(node_textures):
                    new_puppet.textures.append(old_puppet.textures[tex])
                    node.get("textures")[i] = index + i

    def move_node(self, parent, node, new_parent):
        new_puppet = self
        old_puppet = self

        # Retrieving src/dest puppet
        if isinstance(parent, NodeData):
            old_puppet = parent.puppet
            parent_root = parent.root
        else:
            parent_root = parent
        if isinstance(new_parent, NodeData):
            new_puppet = new_parent.puppet
            new_parent_root = new_parent.root
        else:
            new_parent_root = new_parent
        if parent_root == new_parent_root:
            return

        new_puppet.add_node(new_parent, node)
        old_puppet.remove_node(parent, node)
    
    def remove_node(self, parent, node):
        puppet = self
        child_puppet = self
        if isinstance(parent, NodeData):
            puppet = parent.puppet
            parent = parent.root
        if isinstance(node, NodeData):
            child_puppet = node.puppet
            node = node.root
        if puppet != child_puppet:
            return
        parent.get("children").remove(node)
        new_puppet._nodes.remove(node)

    def param(self, name=None, uuid=None):
        res_type = "param"
        return _resources(self, self.root.get(res_type), res_type, ParamData, name, uuid)
    
    def add_param(self, param):
        # Adding param to puppet
        # Validating all link are valid (by referring uuid)
        pass
    
    def remove_param(self, param):
        # Removing param from puppet
        # Validating all link are valid or not.
        pass

    
class NodeData:
    def __init__(self):
        self.res_type="nodes"

    def __repr__(self):
        return "%s(name='%s', uuid='%x')"%(self.res_type, self.root.get("name"), self.root.get("uuid"))
    
    def textures(self):
        if not self.puppet or not isinstance(self.root, dict):
            return None
        if "textures" not in self.root:
            return None
        return [self.puppet.textures[tex] for tex in self.root.get("textures")]

    def add_child(self, node):
        self.puppet.add_node(self, node)
    
    def move_child_to(self, node, new_parent):
        self.puppet.move_child(self, node, new_parent)
    
    def remove_child(self, node):
        self.puppet.remove_node(self, node)
    
    @classmethod
    def from_json(klass, puppet, node_json):
        self = klass()
        self.puppet = puppet
        self.root = node_json
        return self

    
class ParamData(NodeData):
    def __init__(self):
        self.res_type = "param"

    def links(self, name=None, uuid=None):
        res_type = "links"
        return _resources(self, self.root.get(res_type), res_type, LinkData, name, uuid)
    
    def clear_links_for(self, uuid):
        pass

    @classmethod
    def from_json(klass, puppet, param_json):
        self = klass()
        self.puppet = puppet
        self.root = param_json
        self.res_type="param"
        return self


class LinkData(NodeData):
    def __init__(self):
        self.res_type="links"

    @classmethod
    def from_json(klass, puppet, param_json):
        self = klass()
        self.puppet = puppet
        self.root = param_json
        return self
