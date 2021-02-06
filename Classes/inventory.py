class Item:
    def __init__(self, name, type, description, props):
        self.name = name
        self.type = type
        self.description = description
        self.props = props

    def generate_prop(self):
        return self.props