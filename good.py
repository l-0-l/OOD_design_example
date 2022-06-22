import os  # For sending clear screen command
from time import sleep  # For having some delay between rounds

""" This program is an OOD take on the program in the "bad.py" file. Have a look there to see how
the same operation can be achieved without all the classes and stuff. Still, this one's "good", and
the reason for that is also explained there. Eventually, you decide what's "good" and "bad" for your
specific design, clearly not every piece of code should be this extensive. There are many tasks you
can achieve without going into all this typing. As an example, though, this is the right way of
doing things, especially when you work in a team. """


class Movable:
    """ This is a class that defines any movable thing (in the context of this example). """

    def __init__(self, location=(0, 0), direction=(0, 0)):
        """ There are two PRIVATE attributes (prefixed with an underscore character)
        to this class, as such they are not available outside of it. Both attributes are
        stored as tuples of two variables each. This is called encapsulation, look it up. """
        self._location = location  # An (x, y) tuple
        self._direction = direction  # A (dx, dy) tuple, indicates deltas the subject moves with every step

    def get_location(self):
        """ A simple getter for location, so that other classes can access the private attribute. Why do we
        need a getter method? Because other classes do not know we even have such a private attribute. We may
        decide to store it in two separate attributes, for example, but the getter will return a tuple. """
        return self._location

    def set_location(self, location):
        """ A simple setter for location, so other classes can change it externally as well. Why do
        we need a setter method? Why not just make the attribute public (i.e. without the underscore prefix? Because
        we may want to verify that the location is within some range in this function, for example, instead
        of letting any class put any value in it and break our concept. """
        self._location = location

    def get_direction(self):
        """ A getter for the direction tuple. As we have two directions, this is a 2D example, with 9 possible
        directions the movable can walk to - each direction can get values -1, 0, and 1. """
        return self._direction

    def set_direction(self, direction):
        """ A setter for the direction tuple. Minding the comment for the previous setter, here we could check if
        the dx, dy values somebody provided here are not greater than the maximum step distance of our subject. """
        self._direction = direction

    def next_location(self):
        """ Simply put, this method does what it is named for - returns the next location if the movable object
        will take a step from its current location in the current direction. """
        x, y = self._location
        dx, dy = self._direction
        x += dx
        y += dy
        return x, y

    def move(self, *args):
        """ This makes one step of the movable subject, it uses the set_location() and next_location() methods
        for that. There's one thing interesting about this method here, it is the *args parameter. Why do we
        need it? Well, further on a child class will have a move method as well, and will want to call this
        class's move method in turn. But the child's move has an additional parameter, one that this move
        method doesn't have. According to the LSP (Liskov Substitution Principle, look it up) the signatures
        of both methods with the same name in father and child class must be the same. The trick here is,
        therefore, to add the *args parameter, that accepts any number of parameters provided to the method. """
        self.set_location(self.next_location())


class Thing:
    """ This class describes a thing. Any thing. In the scope of this example, it defines the thing's shape. """

    def __init__(self, shape="O"):
        """ One private attribute is defined, the default shape is the letter "O". We didn't discuss this
        till this point, but the __init__ method is important for all non-static classes, and usually we define
        attributes and defaults in it. We don't have to do it, but it is quite useful. The method is then being
        automatically called upon object instantiation, i.e. when we create an object of a specific class. """
        self._shape = shape

    def get_shape(self):
        """ A getter for the shape. This class could include more attributes, and thus more getters/setters. """
        return self._shape

    def set_shape(self, shape):
        """ A setter for the shape. In this example the thing's shape is one character, and we verify that. """
        if len(shape) == 1:
            self._shape = shape


class Place:
    """ The class Place defines the place we act in. This is our subject's environment. The subject will be able
    to move around the place. """

    def __init__(self, borders=(10, 10)):
        """ There's one attribute in the place, at least in this example, and this is its borders. The default
        size of our place is 10x10. """
        self._borders = borders

    def get_borders(self):
        """ A getter for borders. """
        return self._borders

    def set_borders(self, borders):
        """ A setter for borders. """
        self._borders = borders

    def is_within_borders(self, position):
        """ This method verifies that a coordinate received is within the borders of the place. It acts
        on the two variables of the position tuple with square brackets, and returns either True or False. """
        return 0 <= position[0] < self._borders[0], 0 <= position[1] < self._borders[1]

    def get_value(self, location):
        """ Here we return a value of what exists in a specific location of the place. For a game it can be
        grass or stone or a wall, and for that the place must hold a 2D map with different values for each.
        In the scope of this example, we just return a dot for any location. This practically makes this method
        static, i.e. one that does not access internal class resources. Still, we don't mark it as such,
        because the idea behind it is that it COULD return other values as well. """
        return "·"


class Creature(Movable, Thing):
    """ Here we define a creature. We do this by using class inheritance (look it up), so this class inherits
    from two classes defined previously (not all languages allow multiple inheritance). You can look at the
    inheritance as "is a" thing. The creature is a movable. The creature is a thing. But the creature is not
    a place, and therefore it doesn't inherit from Place. We will put a creature in a place later on. """

    def __init__(self):
        """ Since we inherit from other classes, we must call their __init__ methods upon __init__. """
        Movable.__init__(self)
        Thing.__init__(self)

    def move(self, place):
        """ Our creature will move in a certain way. We could make it move randomly, or hunt for food, but
        in this example it will bounce off the walls. The entire creature movement for every step is
        described in ths method. """
        can_move_x, can_move_y = place.is_within_borders(self.next_location())
        if not can_move_x:
            dx, dy = self.get_direction()
            dx = -dx
            self.set_direction((dx, dy))
        if not can_move_y:
            dx, dy = self.get_direction()
            dy = -dy
            self.set_direction((dx, dy))
        super().move()  # This call to super means that a move method of an inherited class will be called


class Screen:
    """ This is our screen. Note that, while this class draws everything in text mode and pretty ugly,
    it could initialize a graphical environment and draw the board and the creature with nice sprites
    on top of it, including animation and so on. Here we see the cool feature of separating the
    responsibilities - other classes that describe the place and the creature have no idea where and
    how it will finally be drawn, if at all. The screen class also does not know what a creature is,
    it just calls its relevant methods to get information. So the class can be extended to use, for
    instance, the PyGame library to draw graphics. In this example, because it is very simple, it is
    a static class - it has no internal attributes at all. All of its functions are marked as such with
    the @staticmethod thingy. """

    @staticmethod
    def clear():
        """ This will clear the screen, replace the command with "clear" for Linux OS. """
        os.system('cls')

    @staticmethod
    def draw(place, creature):
        """ This method draws our board on the screen in text mode. """
        Screen.clear()
        size_x, size_y = place.get_borders()
        for y in range(size_y):
            for x in range(size_x):
                if (x, y) == creature.get_location():
                    print(creature.get_shape() + " ", end="")
                else:
                    print(place.get_value((x, y)) + " ", end="")
            print()


class Game:
    """ Finally, the game class itself. This is not really a game, but it could be. It does its own playing. """

    def __init__(self):
        """ Here we instantiate all the needed classes to real objects. Since a class is, as it usually said,
        a blueprint for an object (do you even know what a blueprint is? look it up!), we can create any number
        of objects of the types defined in classes. When the objects have been created, we begin manipulating
        them using their getters and setters. Pay attention to the double parenthesis in some calls below - this
        is because we actually pass one variable, a tuple, in a form of, say, (x, y) to a method."""
        self.creature = Creature()
        self.place = Place((13, 10))
        self.creature.set_direction((1, 1))
        self.creature.set_location((3, 1))

    def play(self):
        """ This is an endless loop of the "game". The only thing it has to do is to redraw the screen and to
        allow the creature to move. In more complex games you will find more sophisticated actions and controls
        here, but generally it should still remain simple, as all the work is done by the relevant objects and
        their interactions (like the creature changing the direction when hitting a wall here)."""
        while True:
            Screen.draw(self.place, self.creature)
            sleep(0.5)
            self.creature.move(self.place)


""" This starts our software by instantiating the Game class to an object and calling its play() method.
Press Ctrl+C to stop. """
game = Game()
game.play()
