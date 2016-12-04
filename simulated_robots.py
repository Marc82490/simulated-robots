import math
import random
import pylab

#~ random.seed(0)                         # Debugging statement
# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.cleaned_tiles = []
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        tile_x = int(pos.getX())
        tile_y = int(pos.getY())
        if [tile_x, tile_y] not in self.cleaned_tiles:
            self.cleaned_tiles.append([tile_x, tile_y])

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if [m, n] in self.cleaned_tiles:
            return True
        else:
            return False
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        width = self.width
        height = self.height
        return width * height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.cleaned_tiles)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        random_x = random.uniform(0, self.width)
        random_y = random.uniform(0, self.height)
        return Position(random_x, random_y)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        x = pos.getX()
        y = pos.getY()
        
        if x < self.width and x >= 0:
            if y < self.height and y >= 0:
                return True
            else:
                return False
        else:
            return False


# === Problem 2
class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.position = self.room.getRandomPosition()
        self.direction = random.randint(0, 361)
        self.room.cleanTileAtPosition(self.position)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!


# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # Create a Position instance using the robot's current position.
        current_position = self.getRobotPosition()
        angle = self.getRobotDirection()
        # Create a new Position instance based on robot's current position
        #  and direction.
        new_position = current_position.getNewPosition(angle, self.speed)
        # Test whether the new Position instance is in the room.
        if self.room.isPositionInRoom(new_position):
            # If it is, set the robot's position to the new location
            self.setRobotPosition(new_position)
            #  and clean the tile it's now on.
            self.room.cleanTileAtPosition(new_position)
        # If the new Position is not in the room, instead select a new direction.
        else:
            self.setRobotDirection(random.randint(0, 361))


# === Problem 4
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type, visualize):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.
    
    Visualization is turned on when boolean VISUALIZE is set to True.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
        NOTE: THIS WILL NOT WORK WITH min_coverage = 1.0 DUE TO FLOATING POINT ERROR
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    visualize: a boolean to turn on animation
    """
    # Record the number of time steps for all trials.
    time_steps = 0
    
    for trial in range(num_trials):
        if visualize:
            # Create visualization of the current room with robots.
            anim = ps2_visualize.RobotVisualization(num_robots, width, height, delay=0.01)
        # Create a new room for each trial.
        sim_room = RectangularRoom(width, height)
        # Record the number of time steps for this trial.
        timer = 0
        
        # Create a list of robots for this trial.
        robot_list = []
        for robot in range(num_robots):
            robot_list.append(robot_type(sim_room, speed))
            
        percent_cleaned = 0.0
        
        # Clean the room until it passes the minimum coverage threshold.
        while percent_cleaned <= min_coverage:
            if visualize:
                # Update the animation.
                anim.update(sim_room, robot_list)
            # In each loop, move each robot in the trial once and clean their tiles.
            for sim_robot in robot_list:
                sim_robot.updatePositionAndClean()
            # Update progress and increment the time step counter.
            percent_cleaned = sim_room.getNumCleanedTiles() / sim_room.getNumTiles()
            timer += 1
        # Increase the total number of time steps across all trials.
        time_steps += timer
        if visualize:
            # Animation stops at end of trial. Closing it starts the next trial.
            anim.done()
    
    # Return the average number of time steps per trial.       
    return time_steps / num_trials
            

# Uncomment this line to see how much your simulation takes on average.
#~ print(runSimulation(2, 3.0, 10, 10, .9, 30, StandardRobot, False))


# === Problem 5
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # Create a Position instance using the robot's current position.
        current_position = self.getRobotPosition()
        angle = self.getRobotDirection()
        # Create a new Position instance based on robot's current position
        #  and direction.
        new_position = current_position.getNewPosition(angle, self.speed)
        # Test whether the new Position instance is in the room.
        if self.room.isPositionInRoom(new_position):
            # If it is, set the robot's position to the new location
            self.setRobotPosition(new_position)
            #  and clean the tile it's now on.
            self.room.cleanTileAtPosition(new_position)
            # Choose a new direction at random.
            self.setRobotDirection(random.randint(0, 361))
        # If the new Position is not in the room, instead select a new direction.
        else:
            self.setRobotDirection(random.randint(0, 361))


# Uncomment this line to see how much your simulation takes on average.
#~ print(runSimulation(2, 3.0, 10, 10, .9, 30, RandomWalkRobot, True))


def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print("Plotting", num_robots, "robots...")
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot, False))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot, False))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

    
def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300//width
        print("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot, False))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot, False))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    

# === Problem 6
# NOTE: If you are running the simulation, you will have to close it 
# before the plot will show up.

#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
title = "Comparison of Robot Types"
x_label = "Number of Robots"
y_label = "Average Number of Time Steps"

#~ plot_1 = showPlot1(title,x_label, y_label)

#
# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
title = "Comparison of Room Types"
x_label = "Room Aspect Ratios"
y_label = "Average Number of Time Steps"

#~ plot_2 = showPlot2(title, x_label, y_label)
