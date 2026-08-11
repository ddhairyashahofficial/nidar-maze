#!/usr/bin/env python3

import yaml
from pathlib import Path
from collections import deque

# ============================================================
# NIDAR AIR MOUSE - BUILDING STYLE ARENA
# ============================================================

SURVIVOR_CONFIG = (
    Path(__file__).resolve().parent.parent
    / "worlds/layouts/survivors.yaml"
)

def create_survivors():

    with open(SURVIVOR_CONFIG, "r") as f:
        data = yaml.safe_load(f)

    result = ""

    for survivor in data["survivors"]:

        sid = survivor["id"]
        x = survivor["x"]
        y = survivor["y"]
        z = survivor["z"]

        result += f"""
        <model name="{sid}">

            <static>true</static>

            <pose>
                {x} {y} {z}
                0 0 0
            </pose>

            <link name="body">

                <visual name="torso">

                    <pose>
                        0 0 0.65
                        0 0 0
                    </pose>

                    <geometry>

                        <cylinder>
                            <radius>0.22</radius>
                            <length>0.9</length>
                        </cylinder>

                    </geometry>

                    <material>

                        <ambient>
                            0.1 0.2 0.8 1
                        </ambient>

                        <diffuse>
                            0.1 0.2 0.8 1
                        </diffuse>

                    </material>

                </visual>

                <visual name="head">

                    <pose>
                        0 0 1.25
                        0 0 0
                    </pose>

                    <geometry>

                        <sphere>
                            <radius>0.18</radius>
                        </sphere>

                    </geometry>

                    <material>

                        <ambient>
                            0.8 0.6 0.4 1
                        </ambient>

                        <diffuse>
                            0.8 0.6 0.4 1
                        </diffuse>

                    </material>

                </visual>

            </link>

        </model>
        """

    return result

GRID_SIZE = 1.0

ROWS = 15
COLS = 15

ARENA_WIDTH = 15.0
ARENA_LENGTH = 15.0

WALL_THICKNESS = 0.10
WALL_HEIGHT = 2.50

# 8 ft = 2.4384 m
# We use 2.50 m minimum wall height.
# Net is above this.
NET_HEIGHT = 2.55

# ------------------------------------------------------------
# Floor plan
#
# # = wall
# . = free/navigation space
#
# One character = 1 m × 1 m
# ------------------------------------------------------------

GRID = [
    "###############",
    "#..###..###..##",
    "#..###..###..##",
    "##...........##",
    "##..###.###..##",
    "##...........##",
    "#######.#..####",
    "#######.#..####",
    "#######......##",
    "##......###..##",
    "##...........##",
    "#######.##...##",
    "#######.#######",
    "#####......####",
    "###############",
]

# ------------------------------------------------------------
# Entry / Exit
#
# Same physical point.
# Grid coordinate = row 13, column 7
# ------------------------------------------------------------

ENTRY = (13, 7)


# ============================================================
# VALIDATION
# ============================================================

def validate_grid():

    assert len(GRID) == ROWS

    for row in GRID:
        assert len(row) == COLS

    for r in range(ROWS):
        for c in range(COLS):
            assert GRID[r][c] in "#."

    er, ec = ENTRY

    assert GRID[er][ec] == ".", \
        "Entry/exit must be located in free space."

    # BFS connectivity test
    queue = deque([ENTRY])
    visited = {ENTRY}

    while queue:

        r, c = queue.popleft()

        for dr, dc in [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]:

            nr = r + dr
            nc = c + dc

            if not (0 <= nr < ROWS and 0 <= nc < COLS):
                continue

            if GRID[nr][nc] != ".":
                continue

            if (nr, nc) in visited:
                continue

            visited.add((nr, nc))
            queue.append((nr, nc))

    free_cells = sum(
        row.count(".")
        for row in GRID
    )

    if len(visited) != free_cells:

        disconnected = free_cells - len(visited)

        raise RuntimeError(
            f"Layout is disconnected. "
            f"{disconnected} free cells cannot be reached."
        )

    print("Grid validation: PASS")
    print(f"Free cells: {free_cells}")
    print(f"Reachable cells: {len(visited)}")


# ============================================================
# COORDINATE CONVERSION
# ============================================================

def cell_center(row, col):

    x = -7.0 + col
    y = 7.0 - row

    return x, y


# ============================================================
# SDF WALL
# ============================================================

def create_wall(
    name,
    x,
    y,
    sx,
    sy,
    sz=WALL_HEIGHT,
):

    return f"""
    <model name="{name}">

        <static>true</static>

        <pose>
            {x} {y} {sz / 2.0}
            0 0 0
        </pose>

        <link name="link">

            <collision name="collision">

                <geometry>

                    <box>
                        <size>
                            {sx} {sy} {sz}
                        </size>
                    </box>

                </geometry>

            </collision>

            <visual name="visual">

                <geometry>

                    <box>
                        <size>
                            {sx} {sy} {sz}
                        </size>
                    </box>

                </geometry>

                <material>

                    <ambient>
                        0.35 0.35 0.35 1
                    </ambient>

                    <diffuse>
                        0.45 0.45 0.45 1
                    </diffuse>

                </material>

            </visual>

        </link>

    </model>
"""


# ============================================================
# FLOOR
# ============================================================

def furniture_box(
    name,
    x,
    y,
    sx,
    sy,
    sz,
    color="0.45 0.30 0.18"
):

    return f"""
    <model name="{name}">

        <static>true</static>

        <pose>
            {x} {y} {sz / 2.0}
            0 0 0
        </pose>

        <link name="link">

            <collision name="collision">

                <geometry>

                    <box>
                        <size>
                            {sx} {sy} {sz}
                        </size>
                    </box>

                </geometry>

            </collision>

            <visual name="visual">

                <geometry>

                    <box>
                        <size>
                            {sx} {sy} {sz}
                        </size>
                    </box>

                </geometry>

                <material>

                    <ambient>
                        {color} 1
                    </ambient>

                    <diffuse>
                        {color} 1
                    </diffuse>

                </material>

            </visual>

        </link>

    </model>
    """

def create_desk(name, x, y, rotation=0.0):

    return f"""
    <model name="{name}">

        <static>true</static>

        <pose>
            {x} {y} 0
            0 0 {rotation}
        </pose>

        <link name="link">

            <!-- Desktop -->

            <visual name="desktop">

                <pose>
                    0 0 0.75
                    0 0 0
                </pose>

                <geometry>

                    <box>
                        <size>
                            1.4 0.65 0.10
                        </size>
                    </box>

                </geometry>

                <material>

                    <ambient>
                        0.55 0.35 0.18 1
                    </ambient>

                    <diffuse>
                        0.65 0.42 0.22 1
                    </diffuse>

                </material>

            </visual>


            <!-- Legs -->

            <visual name="leg1">
                <pose>-0.55 -0.22 0.37 0 0 0</pose>

                <geometry>
                    <box>
                        <size>0.08 0.08 0.74</size>
                    </box>
                </geometry>
            </visual>

            <visual name="leg2">
                <pose>0.55 -0.22 0.37 0 0 0</pose>

                <geometry>
                    <box>
                        <size>0.08 0.08 0.74</size>
                    </box>
                </geometry>
            </visual>

            <visual name="leg3">
                <pose>-0.55 0.22 0.37 0 0 0</pose>

                <geometry>
                    <box>
                        <size>0.08 0.08 0.74</size>
                    </box>
                </geometry>
            </visual>

            <visual name="leg4">
                <pose>0.55 0.22 0.37 0 0 0</pose>

                <geometry>
                    <box>
                        <size>0.08 0.08 0.74</size>
                    </box>
                </geometry>
            </visual>


            <collision name="desktop_collision">

                <pose>
                    0 0 0.75
                    0 0 0
                </pose>

                <geometry>

                    <box>
                        <size>
                            1.4 0.65 0.10
                        </size>
                    </box>

                </geometry>

            </collision>

        </link>

    </model>
    """

def create_chair(name, x, y, rotation=0.0):

    return f"""
    <model name="{name}">

        <static>true</static>

        <pose>
            {x} {y} 0
            0 0 {rotation}
        </pose>

        <link name="link">

            <!-- Seat -->

            <visual name="seat">

                <pose>
                    0 0 0.45
                    0 0 0
                </pose>

                <geometry>

                    <box>
                        <size>
                            0.45 0.45 0.10
                        </size>
                    </box>

                </geometry>

                <material>

                    <ambient>
                        0.08 0.08 0.10 1
                    </ambient>

                    <diffuse>
                        0.10 0.10 0.12 1
                    </diffuse>

                </material>

            </visual>


            <!-- Backrest -->

            <visual name="back">

                <pose>
                    0 0.18 0.78
                    0 0 0
                </pose>

                <geometry>

                    <box>
                        <size>
                            0.45 0.10 0.65
                        </size>
                    </box>

                </geometry>

            </visual>


            <!-- Central support -->

            <visual name="support">

                <pose>
                    0 0 0.22
                    0 0 0
                </pose>

                <geometry>

                    <cylinder>
                        <radius>0.05</radius>
                        <length>0.45</length>
                    </cylinder>

                </geometry>

            </visual>


            <collision name="collision">

                <pose>
                    0 0 0.45
                    0 0 0
                </pose>

                <geometry>

                    <box>
                        <size>
                            0.45 0.45 0.10
                        </size>
                    </box>

                </geometry>

            </collision>

        </link>

    </model>
    """

def create_cabinet(name, x, y, sx=0.8, sy=0.4, sz=1.8):

    return furniture_box(
        name,
        x,
        y,
        sx,
        sy,
        sz,
        "0.35 0.38 0.42"
    )

def create_sofa(name, x, y, rotation=0.0):

    return f"""
    <model name="{name}">

        <static>true</static>

        <pose>
            {x} {y} 0
            0 0 {rotation}
        </pose>

        <link name="link">

            <visual name="seat">

                <pose>
                    0 0 0.35
                    0 0 0
                </pose>

                <geometry>

                    <box>
                        <size>
                            1.8 0.7 0.35
                        </size>
                    </box>

                </geometry>

                <material>

                    <ambient>
                        0.08 0.12 0.22 1
                    </ambient>

                    <diffuse>
                        0.10 0.15 0.30 1
                    </diffuse>

                </material>

            </visual>


            <visual name="back">

                <pose>
                    0 0.28 0.75
                    0 0 0
                </pose>

                <geometry>

                    <box>
                        <size>
                            1.8 0.18 0.8
                        </size>
                    </box>

                </geometry>

            </visual>


            <collision name="seat_collision">

                <pose>
                    0 0 0.35
                    0 0 0
                </pose>

                <geometry>

                    <box>
                        <size>
                            1.8 0.7 0.35
                        </size>
                    </box>

                </geometry>

            </collision>

        </link>

    </model>
    """

def create_furniture():

    result = ""

    # ========================================================
    # ROOM / OFFICE AREA 1
    # ========================================================

    result += create_desk(
        "desk_01",
        -5.5,
        5.5
    )

    result += create_chair(
        "chair_01",
        -5.5,
        4.95
    )

    result += create_chair(
        "chair_02",
        -4.5,
        5.5,
        1.57
    )

    result += create_cabinet(
        "cabinet_01",
        -5.65,
        6.65
    )


    # ========================================================
    # ROOM / OFFICE AREA 2
    # ========================================================

    result += create_desk(
        "desk_02",
        0.5,
        5.5
    )

    result += create_chair(
        "chair_03",
        0.5,
        4.95
    )

    result += create_chair(
        "chair_04",
        1.5,
        5.5,
        1.57
    )

    result += create_cabinet(
        "cabinet_02",
        1.5,
        6.65
    )


    # ========================================================
    # ROOM / OFFICE AREA 3
    # ========================================================

    result += create_desk(
        "desk_03",
        5.5,
        5.5
    )

    result += create_chair(
        "chair_05",
        5.5,
        4.95
    )

    result += create_cabinet(
        "cabinet_03",
        6.5,
        6.5
    )


    # ========================================================
    # CENTRAL OPEN OFFICE
    # ========================================================

    result += create_desk(
        "desk_04",
        -1.5,
        2.0
    )

    result += create_desk(
        "desk_05",
        1.0,
        2.0
    )

    result += create_chair(
        "chair_06",
        -1.5,
        1.45
    )

    result += create_chair(
        "chair_07",
        1.0,
        1.45
    )


    # ========================================================
    # LOWER OFFICE
    # ========================================================

    result += create_desk(
        "desk_06",
        3.5,
        -4.0
    )

    result += create_chair(
        "chair_08",
        3.5,
        -4.55
    )

    result += create_cabinet(
        "cabinet_04",
        4.5,
        -4.2
    )


    # ========================================================
    # LOUNGE AREA
    # ========================================================

    result += create_sofa(
        "sofa_01",
        -3.0,
        -4.5
    )

    result += create_sofa(
        "sofa_02",
        -3.0,
        -3.0,
        3.14159
    )


    return result

def create_floor():

    return """
    <model name="floor">

        <static>true</static>

        <pose>0 0 -0.05 0 0 0</pose>

        <link name="link">

            <collision name="collision">

                <geometry>

                    <box>
                        <size>
                            15 15 0.10
                        </size>
                    </box>

                </geometry>

            </collision>

            <visual name="visual">

                <geometry>

                    <box>
                        <size>
                            15 15 0.10
                        </size>
                    </box>

                </geometry>

                <material>

                    <ambient>
                        0.65 0.65 0.65 1
                    </ambient>

                    <diffuse>
                        0.70 0.70 0.70 1
                    </diffuse>

                </material>

            </visual>

        </link>

    </model>
    """


# ============================================================
# GRID FLOOR MARKINGS
# ============================================================

def create_grid_markings():

    result = ""

    count = 0

    # Thin visual lines on the floor.
    # These help us inspect the 1 m modular structure.

    for i in range(-7, 8):

        result += f"""
        <model name="grid_x_{count}">

            <static>true</static>

            <pose>{i} 0 0.006 0 0 0</pose>

            <link name="link">

                <visual name="visual">

                    <geometry>

                        <box>
                            <size>
                                0.008 15 0.002
                            </size>
                        </box>

                    </geometry>

                    <material>

                        <ambient>
                            0.25 0.25 0.25 0.35
                        </ambient>

                    </material>

                </visual>

            </link>

        </model>
        """

        count += 1

    for i in range(-7, 8):

        result += f"""
        <model name="grid_y_{count}">

            <static>true</static>

            <pose>0 {i} 0.007 0 0 0</pose>

            <link name="link">

                <visual name="visual">

                    <geometry>

                        <box>
                            <size>
                                15 0.008 0.002
                            </size>
                        </box>

                    </geometry>

                    <material>

                        <ambient>
                            0.25 0.25 0.25 0.35
                        </ambient>

                    </material>

                </visual>

            </link>

        </model>
        """

        count += 1

    return result


# ============================================================
# WALL GENERATION
# ============================================================

def create_walls():

    result = ""

    wall_id = 0

    for r in range(ROWS):

        for c in range(COLS):

            if GRID[r][c] != ".":
                continue

            x, y = cell_center(r, c)

            # --------------------------------------------
            # North boundary
            # --------------------------------------------

            if r == 0 or GRID[r - 1][c] == "#":

                result += create_wall(
                    f"wall_{wall_id}",
                    x,
                    y + 0.5,
                    GRID_SIZE,
                    WALL_THICKNESS,
                )

                wall_id += 1

            # --------------------------------------------
            # South boundary
            # --------------------------------------------

            if r == ROWS - 1 or GRID[r + 1][c] == "#":

                # Leave the ENTRY/EXIT opening.

                if (r, c) != ENTRY:

                    result += create_wall(
                        f"wall_{wall_id}",
                        x,
                        y - 0.5,
                        GRID_SIZE,
                        WALL_THICKNESS,
                    )

                    wall_id += 1

            # --------------------------------------------
            # West boundary
            # --------------------------------------------

            if c == 0 or GRID[r][c - 1] == "#":

                result += create_wall(
                    f"wall_{wall_id}",
                    x - 0.5,
                    y,
                    WALL_THICKNESS,
                    GRID_SIZE,
                )

                wall_id += 1

            # --------------------------------------------
            # East boundary
            # --------------------------------------------

            if c == COLS - 1 or GRID[r][c + 1] == "#":

                result += create_wall(
                    f"wall_{wall_id}",
                    x + 0.5,
                    y,
                    WALL_THICKNESS,
                    GRID_SIZE,
                )

                wall_id += 1

    return result


# ============================================================
# ENTRY / EXIT MARKER
# ============================================================

def create_entry_marker():

    x, y = cell_center(*ENTRY)

    return f"""
    <model name="entry_exit">

        <static>true</static>

        <pose>
            {x} {y} 0.01
            0 0 0
        </pose>

        <link name="link">

            <visual name="visual">

                <geometry>

                    <box>
                        <size>
                            0.60 0.60 0.01
                        </size>
                    </box>

                </geometry>

                <material>

                    <ambient>
                        0.0 0.8 0.1 1
                    </ambient>

                    <diffuse>
                        0.0 0.8 0.1 1
                    </diffuse>

                </material>

            </visual>

        </link>

    </model>
    """


# ============================================================
# NET
# ============================================================

def create_net():

    result = ""

    spacing = 0.5

    net_id = 0

    # Longitudinal strips

    for i in range(-15, 16):

        x = i * spacing

        result += f"""
        <model name="net_x_{net_id}">

            <static>true</static>

            <pose>
                {x} 0 {NET_HEIGHT}
                0 0 0
            </pose>

            <link name="link">

                <visual name="visual">

                    <geometry>

                        <box>
                            <size>
                                0.008 15 0.008
                            </size>
                        </box>

                    </geometry>

                </visual>

            </link>

        </model>
        """

        net_id += 1

    # Transverse strips

    for i in range(-15, 16):

        y = i * spacing

        result += f"""
        <model name="net_y_{net_id}">

            <static>true</static>

            <pose>
                0 {y} {NET_HEIGHT}
                0 0 0
            </pose>

            <link name="link">

                <visual name="visual">

                    <geometry>

                        <box>
                            <size>
                                15 0.008 0.008
                            </size>
                        </box>

                    </geometry>

                </visual>

            </link>

        </model>
        """

        net_id += 1

    return result


# ============================================================
# SDF WORLD
# ============================================================

def create_world():

    world = """<?xml version="1.0"?>

<sdf version="1.9">

<world name="nidar_airmouse_building">

    <gravity>0 0 -9.81</gravity>

    <plugin
        filename="gz-sim-physics-system"
        name="gz::sim::systems::Physics"/>

    <plugin
        filename="gz-sim-user-commands-system"
        name="gz::sim::systems::UserCommands"/>

    <plugin
        filename="gz-sim-scene-broadcaster-system"
        name="gz::sim::systems::SceneBroadcaster"/>

    <light type="directional" name="sun">

        <pose>
            0 0 10 0 0 0
        </pose>

        <cast_shadows>true</cast_shadows>

        <direction>
            -0.3 0.2 -1.0
        </direction>

    </light>
"""

    world += create_floor()
    world += create_grid_markings()
    world += create_walls()

    # Office environment
    world += create_furniture()

    # Mission objects
    world += create_entry_marker()
    world += create_survivors()

    # Covered arena
    world += create_net()

    world += """
</world>

</sdf>
"""

    return world


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("==========================================")
    print(" NIDAR AirMouse Building Arena Generator")
    print("==========================================")
    print()

    validate_grid()

    output_dir = Path("../worlds/generated")
    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = output_dir / "building_arena.sdf"

    output_file.write_text(
        create_world()
    )

    print()
    print("Arena generated successfully.")
    print()
    print(f"Size          : {ARENA_WIDTH} × {ARENA_LENGTH} m")
    print(f"Grid          : {GRID_SIZE} × {GRID_SIZE} m")
    print(f"Wall height   : {WALL_HEIGHT} m")
    print(f"Net height    : {NET_HEIGHT} m")
    print("Corridor      : 1 m minimum")
    print("Entry / Exit  : same location")
    print()
    print(f"Output:")
    print(output_file)
    print()


if __name__ == "__main__":
    main()
