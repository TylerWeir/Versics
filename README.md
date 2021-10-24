# Versics
A Verlet physics engine for Python.

## Todo
Below is a list of things that need to be addressed

### Collisions
Currently there are no rigid body collisions, only a constraint to keep bodies within the given bounds. Collisions will become much easier with the class layout described above.  The world class will likely be the one to contain the code for the collision handling.  

Some related concepts:
* Broad Phase (collisions of general bounding boxes)
* Narrow Phase (collisions of the actual geometries)
* Sort and Sweep Algorithm

Resources:
* [Collision Detection for Solid Objects](https://www.toptal.com/game/video-game-physics-part-ii-collision-detection-for-solid-objects)
* Jakobsen's Advanced Character Physics

### Functions to make common geometries
It would be really useful to have functions to make entities with common geometries such as squares, triangles, circles, and even mesh(cloth). Functions could take arguments describing the entity such as initial position, velocity, size, mass, orientation, etc. (Some of that may only be described in the world object)

### Masses of points
Jakobsen's paper discusses handling constraints while respecting particle masses. Reference page 9 of his Advanced Character Physics paper. Currently, I don't have a clean way to initialize the points of the object with a mass trait.  An interesting thing to note is he describes fixing points in space by giving them infinite mass. You can then move these infinite masses manually to "force" the entity.

### Cloth
Cloth simulations use the idea that cloth can be pulled but not pushed. To model this, only enforce the stick constraints when the points are pulled too far apart only; not when they are too close.  The Jakobsen paper used a different approach of just interating through the stick constraint once, so that it is weak and allows a proper amount of bend. He said that this worked well for simulating plants. Another thing to note is cloth could be ripped if the sticks have a bound to the distance that they can stretch past their resting length. That is remove the stick constraint if stretched too far.  
