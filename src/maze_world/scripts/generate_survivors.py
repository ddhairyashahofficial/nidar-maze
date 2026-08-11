#!/usr/bin/env python3

from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "worlds/layouts/survivors.yaml"
OUTPUT = ROOT / "worlds/generated/survivors.sdf"


def survivor_model(s):

    return f"""
    <model name="{s['id']}">

        <static>true</static>

        <pose>
            {s['x']}
            {s['y']}
            {s['z']}
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


            <collision name="collision">

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

            </collision>

        </link>

    </model>
    """


def main():

    with open(CONFIG, "r") as f:
        data = yaml.safe_load(f)

    survivors = data["survivors"]

    output = """
<?xml version="1.0"?>

<sdf version="1.9">

<world name="survivors">
"""

    for survivor in survivors:

        output += survivor_model(survivor)

    output += """
</world>

</sdf>
"""

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT.write_text(output)

    print(
        f"Generated {len(survivors)} survivors."
    )

    print(
        f"Output: {OUTPUT}"
    )


if __name__ == "__main__":
    main()
