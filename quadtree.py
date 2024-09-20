from collections import namedtuple

vec = namedtuple('vec', ['x', 'y'])

def divide_vec(point, div):
    return vec(point.x / div, point.y / div)

class AABB:
    def __init__(self, center, ext):
        self.center = center
        self.ext = ext

    def contains(self, point: vec) -> bool:
        ''' check whatever point lies in bounded box'''
        return self.center.x + self.ext.x >= point.x >= self.center.x - self.ext.y and\
            self.center.y + self.ext.y >= point.y >= self.center.y - self.ext.y 

    @property
    def x_start(self):
        return self.center.x - self.ext.x

    @property
    def x_end(self):
        return self.center.x + self.ext.x

    @property
    def y_start(self):
        return self.center.y - self.ext.y

    @property
    def y_end(self):
        return self.center.y + self.ext.y

class QuadTree:
    def __init__(self, aabb = None):
        if not aabb:
            aabb = AABB(vec(50, 50), vec(50, 50))
        self.aabb = aabb
        self.nodes = []
        self.point = None
        self.has_children = False

    def insert(self, point: vec):
        if not self._insert_inner(point):
            raise ValueError("point is not in the range")

    def regroup(self):
        self.has_children = True
        aabb = self.aabb
        center, ext = aabb.center, aabb.ext
        self.nodes.append(QuadTree(AABB(vec((center.x + aabb.x_end) / 2, (center.y + aabb.y_start) / 2), divide_vec(ext,2))))
        self.nodes.append(QuadTree(AABB(vec((center.x + aabb.x_end) / 2, (center.y + aabb.y_end) / 2), divide_vec(ext,2))))
        self.nodes.append(QuadTree(AABB(vec((center.x + aabb.x_start) / 2, (center.y + aabb.y_start) / 2), divide_vec(ext,2))))
        self.nodes.append(QuadTree(AABB(vec((center.x + aabb.x_start) / 2, (center.y + aabb.y_end) / 2), divide_vec(ext,2))))

        if self.point:
            point = self.point
            self.point = None
            self._insert_inner(point)

    def _insert_inner(self, point: vec) -> bool:
        if not self.aabb.contains(point):
            return False
    
        if not self.has_children and self.point is None:
            self.point = point
            return True

        if not self.has_children:
            self.regroup()

        for node in self.nodes:
            if node._insert_inner(point):
                return True

        return False

    def inorder(self):
        for node in self.nodes:
            node.inorder() 

        print(self.point)


