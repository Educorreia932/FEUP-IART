class State():
    
    def __init__(self, starter_backbone):
        self.target_covered = 0
        self.placed_routers = []
        self.placed_backbones = [starter_backbone]
        self.connected_cells = []