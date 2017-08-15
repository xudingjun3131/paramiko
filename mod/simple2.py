class Rectangle():
def _ _init_ _(self, color="white", width=10, height=10):
    print "create a", color, self, "sized", width, "x", height
class RoundedRectangle(Rectangle):
def _ _init_ _(self, **kw):
    Rectangle(._ _init_ _, (self,), kw)
    rect = Rectangle(color="green", height=100, width=100) rect= RoundedRectangle(color="blue",height = 20)< /FONT> <FONT face= 宋体>