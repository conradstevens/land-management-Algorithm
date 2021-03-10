

class Tile:
    x, y, = -1, -1

    char = 'N'
    isSeen = False
    isPlantable = False

    def __init__(self, x, y, char):
        self.x, self.y, = x, y
        self.char = char

        if char == '.':
            self.isPlantable = True
