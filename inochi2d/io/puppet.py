def _resources(puppet, resources, res_type, klass, name=None, uuid=None):
    if resources is None:
        return None
    if name is None and uuid is None:
        return [klass(puppet).from_json(puppet, node) for node in resources]
    elif name is not None:
        return [klass(puppet).from_json(puppet, node) for node in resources if isinstance(node, dict) and name in node.get("name")]
    elif uuid is not None:
        return [klass(puppet).from_json(puppet, node) for node in resources if isinstance(node, dict) and node.get("uuid") == uuid]
    return None


class PuppetData:
    def __init__(self, puppet_json, textures, exts):
        self.textures    = textures
        self.exts        = exts
        self.root        = puppet_json
        
        self._nodes = []
        self.collect_nodes(self.root.get("nodes"))

    def collect_nodes(self, node):
        if not isinstance(node, dict):
            return
        self._nodes.append(node)
        if node.get("children"):
            for child in node.get("children"):
                self.collect_nodes(child)

    def exclude_nodes(self, node):
        if not isinstance(node, dict):
            return
        self._nodes.remove(node)
        if node.get("children"):
            for child in node.get("children"):
                self.exclude_nodes(child)
        
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
        
        new_puppet.collect_nodes(node)
        
        # Validating uniqueness of the uuid
        # Updating UUID, and maintain links if needed.

        # Updating texture slot
        if new_puppet != old_puppet:
            def add_texture_recur(new_puppet, node):
                index = len(new_puppet.textures)
                node_textures = node.get("textures")
                if node_textures:
                    for i, tex in enumerate(node_textures):
                        new_puppet.textures.append(old_puppet.textures[tex])
                        node.get("textures")[i] = index + i
                children = node.get("children")
                if children is not None:
                    for child in children:
                        add_texture_recur(new_puppet, child)
            add_texture_recur(new_puppet, node)

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

        if old_puppet is not None:
            old_puppet.remove_node(parent, node)
        new_puppet.add_node(new_parent, node)
    
    def remove_node(self, parent, node):
        # Updating json information
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

        #Updating _nodes
        puppet.exclude_nodes(node)

    def param(self, name=None, uuid=None):
        res_type = "param"
        return _resources(self, self.root.get(res_type), res_type, ParamData, name, uuid)
    
    def add_param(self, param):
        if isinstance(param, ParamData):
            param = param.root
        # Adding param to puppet
        params = self.root.get("param")
        if params is not None:
            params.add(param)
        param = ParamNode.from_json(self, param)
        return param
    
    def remove_param(self, param):
        # Removing param from puppet
        # Validating all link are valid or not.
        if isinstance(param, ParamData):
            param = param.root
        # Removing param from puppet
        params = self.root.get("param")
        if params is not None:
            params.remove(param)

    def clear_binding(self):
        for p in self.param():
            p.clear_binding()
            
    def cleanup_slot(self):
        # Updating texture slot
        used_slots = set()
        for node in new_puppet._nodes:
            if node.get("textures"):
                for s in node["textures"]:
                    used_slots.append(s)
        textures

    
class NodeData:
    def __init__(self, puppet):
        self.puppet = puppet
        self.res_type="nodes"

    def __repr__(self):
        return "%s(name='%s', uuid='%x')"%(self.res_type, self.root.get("name"), self.root.get("uuid"))
    
    def textures(self):
        if not self.puppet or not isinstance(self.root, dict):
            return None
        if "textures" not in self.root:
            return None
        return [self.puppet.textures[tex] for tex in self.root.get("textures")]
    
    def name(self):
        return self.root.get("name")
    
    def uuid(self):
        return self.root.get("uuid")

    def add_child(self, node):
        self.puppet.add_node(self, node)
    
    def move_child_to(self, node, new_parent):
        self.puppet.move_child(self, node, new_parent)
    
    def remove_child(self, node):
        self.puppet.remove_node(self, node)
    
    @classmethod
    def from_json(klass, puppet, node_json):
        self = klass(puppet)
        self.puppet = puppet
        self.root = node_json
        return self

    
class ParamData(NodeData):
    def __init__(self, puppet):
        self.puppet = puppet
        self.res_type = "param"

    def links(self, name=None, uuid=None):
        res_type = "links"
        return _resources(self, self.root.get(res_type), res_type, LinkData, name, uuid)
    
    def clear_links_for(self, uuid):
        pass

    @classmethod
    def from_json(klass, puppet, param_json):
        self = klass(puppet)
        self.puppet = puppet
        self.root = param_json
        self.res_type="param"
        return self

    def clear_binding(self):
        is_vec2 = self.root.get("is_vec2")
        bindings = self.root.get("bindings")
        
        def check_existence(b):
            node = self.puppet.nodes(uuid=b.get("node"))
            if len(node) == 0:
                print("No node %x of binding %s"%(b.get("node"), self.root.get("name")))
                return False
            node = node[0]
            if b.get("param_name") == "deform":
                target = b.get("values")[0]
                target = target[0]
                verts = node.root.get("mesh").get("verts")
                if len(target) != len(verts) / 2:
                    print("Number of mesh of '%s'(%d) != '%s'(%d)"%(self.root.get("name"), len(target), node.root.get("name"), len(verts)))
                    return False
            return True

        if bindings is not None:
            self.root["bindings"] = [b for b in bindings if check_existence(b)]
                
    
    def merge_binding(self, overwrite):
        is_vec2 = self.root.get("is_vec2")
        bindings = self.root.get("bindings")
        ow_bindings = overwrite.root.get("bindings")
        not_matched = []
        
        axis_points = self.root.get("axis_points")
        ow_axis_points = overwrite.root.get("axis_points")

        if len(axis_points[0]) != len(ow_axis_points[0]) or\
           len(axis_points[1]) != len(ow_axis_points[1]):
            print("Axis points of '%s' differs from '%s', replace all."%(self.root.get("name"), overwrite.root.get("name")))
            self.root.clear()
            self.root.update(overwrite.root)
        
        else:
            for ow_b in ow_bindings:
                b = [bb for bb in bindings if bb.get("node") == ow_b.get("node") and bb.get("param_name") == ow_b.get("param_name")]
                if len(b) > 0:
                    b[0].clear()
                    b[0].update(ow_b)
                else:
                    print("%s is not in original. Added."%self.puppet.nodes(uuid=ow_b.get("node")))
                    not_matched.append(ow_b)
            bindings.extend(not_matched)
            
    def add_link(self, link = None, param = None):
        if link is None and param is not None:
            if isinstance(param, ParamData):
                param = param.root
            link = LinkData(self.puppet, param.get("uuid"))
        if isinstance(link, LinkData):
            link = link.root
        if "links" not in self.root:
            self.root["links"] = []
        self.root["links"].append(link)
    
    def remove_link(self, link):
        if isinstance(link, LinkData):
            link = link.root
        if "links" in self.root:
            self.root["links"].remove(link)
        
                

class BindingData(NodeData):
    def __init__(self, puppet):
        self.puppet = puppet
        self.res_type="bindings"
        self.root = {
            "node": None,
            "param_*name": "",
            "values": [[]],
            "isSet": [[]],
            "interpolate_mode": ""
        }

    @classmethod
    def from_json(klass, puppet, param_json):
        self = klass(puppet)
        self.puppet = puppet
        self.root = param_json
        return self
                

class LinkData(NodeData):
    def __init__(self, puppet, link_uuid = None):
        self.puppet = puppet
        self.res_type="links"
        self.root = {
            "linkUUID": link_uuid,
            "inAxis": 0,
            "outAxis": 0
        }

    @classmethod
    def from_json(klass, puppet, param_json):
        self = klass(puppet)
        self.puppet = puppet
        self.root = param_json
        return self
