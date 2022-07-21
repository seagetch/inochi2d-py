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
    
    def _resources(self, resources, res_type, klass, name=None, uuid=None):
        if name is None and uuid is None:
            return [klass(node) for node in resources]
        elif name is not None:
            return [klass(node) for node in resources if isinstance(node, dict) and name in node.get("name")]
        elif uuid is not None:
            return [klass(node) for node in resources if isinstance(node, dict) and node.get("uuid") == uuid]
        return None

    def nodes(self, name=None, uuid=None):
        return self._resources(self._nodes, "nodes", NodeData, name, uuid)

    def param(self, name=None, uuid=None):
        res_type = "param"
        return self._resources(self.root.get(res_type), res_type, ParamData, name, uuid)

    def links(self, name=None, uuid=None):
        res_type = "links"
        return self._resources(self.root.get(res_type), res_type, LinkData, name, uuid)
    
class NodeData:
    def __init__(self, node_json):
        self.root = node_json

    def __repr__(self):
        return "Node(name='%s', uuid='%x')"%(self.root.get("name"), self.root.get("uuid"))

class ParamData:
    def __init__(self, param_json):
        self.root = param_json

    def __repr__(self):
        return "Param(name='%s', uuid='%x')"%(self.root.get("name"), self.root.get("uuid"))

class LinkData:
    def __init__(self, node_json):
        self.root = node_json

    def __repr__(self):
        return "Link(name='%s', uuid='%x')"%(self.root.get("name"), self.root.get("uuid"))
