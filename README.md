# NIDAR AirMouse — Layer 1 Gazebo Maze

This package contains ONLY the structural Layer 1 arena:
- 15 m x 15 m floor
- 14 x 14 logical maze grid
- 1.00 m clear passages
- 0.05 m wall thickness
- 2.50 m wall height
- four 2x2 logical room modules
- one south-side entry/exit opening
- no furniture
- no debris
- no survivors
- no drone
- no sensors

## Run

Install Gazebo Harmonic / gz-sim, then:

```bash
gz sim /path/to/nidar_layer1_maze/nidar_maze.sdf
```

## Geometry convention

The structural wall-center spacing is 1.05 m:
1.05 m center-to-center - 0.025 m - 0.025 m = 1.00 m clear passage.

The 14x14 structural grid occupies 14.70 m, centered inside the 15 m arena.
