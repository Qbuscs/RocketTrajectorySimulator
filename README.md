# Getting started
This is a simple script for simulating a rocket's trajectory in a solar system. The position of planets
is calculated based on input date, and get from [solarsystem](https://github.com/IoannisNasios/solarsystem) library. Once ran, the planet data is saved to planets.picle, as it is not affected by anything during the simulation, and there is no need to recalculate it every time there is a change to other starting parameters. If you want to change the takeoff date however, you need to delete this file manually so that movement of celestial bodies can be calculated anew.

This is simillar to N-body problem, with a distinction that rocket is not massive enough to influence planets' course, so that kind of interaction is ignored. Moreover, we can controll the movement of a space ship with an engine burn manouvers, which will change its velocity in a given direction at a cost of burning fuel and thus reducing its mass.

A rocket is defined by following parameters:
* Mass of a rocket itself \[kg\]
* Mass of fuel \[kg\]
* Engine force \[N\]
* Engine Isp
* Starting possition
* Starting velocity

All starting parameters are in a main.py file, so you can change them to your liking there, as I can't be bothered to make a functional interface or args reading from command line.

# Things to improve
* Currently the simulation step is set to 1 minute. Higher steps are unstable when the rocket is closly orbiting a celestial body. However on interplanetary trajectory, this could be dynamically increased to probably over 1 hour, as the change in forces affecting the rocket is not that big.
* When you run this simulation, look at the results, and want to add a burn maneuver at some point, you shouldn't have to rerun the simulation up to this point. This is, however, excactly what happens, so possible fix is to remember the trajectory up to added engine burn moment