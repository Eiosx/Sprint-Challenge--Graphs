from room import Room
from player import Player
from world import World
from queue import Queue
from stack import Stack
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
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

opposite_directions = {"n": "s", "w": "e", "e": "w", "s": "n"}
# Graph


class Graph:
    def __init__(self):
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
            if value != "?":
                neighbor_list.append((key, value))
        return neighbor_list

    def get_path(self, start, end, visited=None, path=None):
        if visited is None:
            visited = set()
        if path is None:
            path = []
        path = path + [start]
        if start in end:
            return path
        if start not in visited:
            visited.add(start)
            for neighbor in self.get_neighbors(start):
                new_path = self.get_path(neighbor[1], end, visited, path)
                if new_path:
                    return new_path
        return None


class Traversal:
    def __init__(self, player):
        self.player = player
        self.maze = Graph()
        self.searched = set()
        opposite_directions = {"n": "s", "w": "e", "e": "w", "s": "n"}
        self.directions = {}
        self.other_rooms = []

    def next_direction(self, room):
        for direction in self.directions:
            if direction in self.maze.vertices[room]:
                if self.maze.vertices[room][direction] == '?':
                    return direction
        return None

    def go_back(self, room):
        if len(self.other_rooms) == 0:
            return None
        end = self.other_rooms
        new_path = self.maze.get_path(room, end)
        return new_path

    def look_for_exit(self, room):
        for exits in self.maze.vertices[room]:
            if self.maze.vertices[room][exits] == '?':
                if room not in self.other_rooms:
                    self.other_rooms.append(room)
                return False
        self.searched.add(room)
        if room in self.other_rooms:
            self.other_rooms.remove(room)
        return True

    def create_room(self, room, room_exits):
        for room_exit in room_exits:
            self.maze.add_vertex(room, room_exit)

    def move_forward(self):
        room = self.player.current_room.id
        room_exits = self.player.current_room.get_exits()

        if room not in self.maze.vertices:
            self.create_room(room, room_exits)

        if room not in self.searched and self.look_for_exit(room):
            self.searched.add(room)

        next_direction = self.next_direction(room)
        if next_direction is not None:
            self.player.travel(next_direction)
            traversal_path.append(next_direction)
            next_room = self.player.current_room.id
            next_room_exits = self.player.current_room.get_exits()
            if next_room not in self.maze.vertices:
                self.create_room(next_room, next_room_exits)
            self.maze.add_edge(room, next_room, next_direction)
            self.look_for_exit(room)

    def generate_graph(self, room=None, graph=None, player=None, queue=None):
        if graph is None:
            graph = Graph()
        if player is None:
            player = Player(world.starting_room)
        if queue is None:
            queue = Queue()
        if room is None:
            room = player.current_room
        room_exits = player.current_room.get_exits()
        if room.id not in graph.vertices:
            for room_exit in room_exits:
                graph.add_vertex(room.id, room_exit)
        for direction in graph.vertices[room.id]:
            queue.enqueue((direction, room))

        while len(queue) > 0:
            next_move = queue.dequeue()
            direction = next_move[0]
            room = next_move[1]

            next_room = room.get_room_in_direction(direction)
            next_room_exits = room.get_room_in_direction(direction).get_exits()
            if next_room.id not in graph.vertices:
                for r_exit in next_room_exits:
                    graph.add_vertex(next_room.id, r_exit)
            graph.add_edge(room.id, next_room.id, direction)
            for r_exit in graph.vertices[next_room.id]:
                if graph.vertices[next_room.id][r_exit] == '?':
                    queue.enqueue((r_exit, next_room))

    def traverse(self):
        direction_list = ['n', 'w', 'e', 's']
        for direction in direction_list:
            self.directions[direction] = direction
        room = self.player.current_room.id
        room_exits = self.player.current_room.get_exits()

        if room not in self.maze.vertices:
            for exit in room_exits:
                self.maze.add_vertex(room, exit)

        while len(self.searched) != len(room_graph):

            rooms_searched = self.look_for_exit(room)
            if not rooms_searched and room not in self.other_rooms:
                self.other_rooms.append(room)

            while not rooms_searched:
                self.move_forward()
                room = self.player.current_room.id
                rooms_searched = self.look_for_exit(room)

            while rooms_searched:
                get_path_to_next_advance = self.go_back(room)

                if get_path_to_next_advance is not None:
                    current_rooms = get_path_to_next_advance[:-1]
                    next_rooms = get_path_to_next_advance[1:]

                    next_dirs = []
                    for i in range(len(get_path_to_next_advance) - 1):
                        cur_room = current_rooms[i]
                        nex_room = next_rooms[i]
                        for direction in self.maze.vertices[cur_room]:
                            if self.maze.vertices[cur_room][direction] == nex_room:
                                next_dirs.append(direction)
                    for backtrack_direction in next_dirs:
                        self.player.travel(backtrack_direction)
                        traversal_path.append(backtrack_direction)
                    room = self.player.current_room.id
                    rooms_searched = self.look_for_exit(room)
                else:
                    break


traverse_graph = Traversal(player)
traverse_graph.traverse()


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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
