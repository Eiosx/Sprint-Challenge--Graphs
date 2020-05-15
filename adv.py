from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

opposite_directions = {"n" : "s", "w" : "e", "e" : "w", "s" : "n"}
# Graph

class Graph:
  def_init_(self):
    self.vertices = {}

  def add_vertex(self, room, direction):
    if room not in self.vertices:
      self.vertices[room] = {}
    self.vertices[room][direction] = "?"
  
  def add_edge(self, room1, room2, direction):
    self.vertices[room1][direction] = room2
    self.vertices[room2][opposite_directions[direction]] = room1

  def get_neighbors(self, room):
    neighbor_list = []
    for key, value in self.vertices[room].items():
      if value not "?":
        neighbor_list.append((key, value))
    return neighbor_list


class Traversal:
    def __init__(self, player):
        self.player = player
        self.maze = Graph()
        self.finished = set()
        opposite_directions = {"n" : "s", "w" : "e", "e" : "w", "s" : "n"}


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
