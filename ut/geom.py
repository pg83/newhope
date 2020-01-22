class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add_vector(self, dx, dy):
        return Point(self.x + dx, self.y + dy)

    
class Rect(Point):
    def __init__(self, p, w, h):
        Point.__init__(self, p.x, p.y)
        self.w = w
        self.h = h

    def add_border(self, w=1, h=1):
        return Rect(self.add_vector(w, h), self.w - 2 * w, self.h - 2 * h)

    def to_virtual(self):
        return Rect(Point(0, 0), self.w, self.h)

    def set_width(self, w):
        return Rect(self, w, self.h)
    
    def set_height(self, h):
        return Rect(self, self.w, h)

    def inc_height(self, h=1):
        return self.set_height(self.h + h)
    
    def dec_height(self, h=1):
        return self.set_height(self.h - h)
    
    def move(self, dx, dy):
        return Rect(self.add_vector(dx, dy), self.w, self.h)

    def move_down(self, dy):
        return self.move(0, dy)
    
    def move_up(self, dy):
        return self.move(0, -dy)
    
    def move_right(self, dx):
        return self.move(dx, 0)
    
    def move_left(self, dx):
        return self.move(-dx, 0)
    
    def __str__(self):
        return str([self.x, self.y, self.w, self.h])
    
    
def wh_rect(w, h):
    return Rect(Point(0, 0), w, h)
