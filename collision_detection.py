# This class is used to handle collision detection between entities
#

from versics import Entity
from pygame.math import Vector2

# should it extend entity? I'm thinking yes
class Collision_Detector():
    """Used to detect collisions between Entities."""

    def __init__(self):
        # Traits needed for broad phase collision detection
        self.size = () # dimensions of rectangular bounding box
        self.pos = Vector2() # position of the top left corner of the box

    def make_bounding_box(self):
        """Makes a bounding box around the entity used for broad phase
        collision detection."""
        pass

    def broad_phase_collision(self, other_entity):
        """Returns true if there is a broad phase collision with a
        given entity."""

        # Going to use axis aligned bounding boxes
        #
        # Either will rotate with the object or need to be calculated with
        # every frame to work with non rigid bodies such as ropes and cloth

        #C code for bounding box collisions
        """
        BOOL TestAABBOverlap(AABB* a, AABB* b)
{
    float d1x = b->min.x - a->max.x;
    float d1y = b->min.y - a->max.y;
    float d2x = a->min.x - b->max.x;
    float d2y = a->min.y - b->max.y;

    if (d1x > 0.0f || d1y > 0.0f)
        return FALSE;

    if (d2x > 0.0f || d2y > 0.0f)
        return FALSE;

    return TRUE;
}"""

        pass

    def narrow_phase_collision(self, other_entity):
        """Returns true if there is a narrow phase collision with a
        given entity."""
        pass


    def broad_phase(entities):
        """Identifies which entities are in broad phase collision."""
        # Public function which takes a list of all entities and then somehow
        # returns the entities which are in broad phase collision with one
        # another
        #
        # This will likely include the sort and sweep algorithim
