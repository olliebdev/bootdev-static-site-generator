class HTMLNode:
    def __init__(self, tag=None, text=None, children=None, props=None):
        self.tag = tag
        self.text = text
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        s = " "
        for key, value in self.props.items():
            s += f'{key}="{value}" '
        return s.rstrip()

    def __repr__(self):
        return f"HTMLNode(tag='{self.tag}', text='{self.text}', children='{self.children}', props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, text, props=None):
        super().__init__(tag, text, [], props)

    def to_html(self):
        if self.text is None:
            raise ValueError("Value cannot be None.")
        if self.tag is None:
            return str(self.text)
        props_str = " ".join(
            f'{key}="{value}"' for key, value in (self.props or {}).items()
        )
        if props_str:
            return f"<{self.tag} {props_str}>{self.text}</{self.tag}>"
        return f"<{self.tag}>{self.text}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is required")
        if self.children is None:
            raise ValueError("Children requires a value")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
