print("JUST TESTING")

import pygame
import pymunk
import pymunk.pygame_util
from colorama import Fore

print(Fore.BLUE + "$15 FOR FUCKING BLUE!?!?!? ")
print(Fore.CYAN + "ARE YOU OUT OF YOUR MIND?!?!?!111!!11")

run_once = 0

pygame.init()
screen = pygame.display.set_mode((1200, 900))
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0, 900)
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Mouse Dragging
mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
dragged_joint = None
dragged_shape = None


# Create a static floor
floor = pymunk.Segment(space.static_body, (0, 580), (800, 580), 5)
floor.elasticity = 0.5
# floor.friction = 1.0 # WTF?
# floor.friction = 0.1 # WTF?
space.add(floor)


# Stickman body (a simple circle for head, segments for limbs)
def create_stickman_old(space, x, y):
    # Head
    head_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 15))
    head_body.position = x, y
    head_shape = pymunk.Circle(head_body, 15)
    head_shape.elasticity = 0.5
    space.add(head_body, head_shape)

    # Torso
    torso_body = pymunk.Body(2, pymunk.moment_for_segment(2, (0, 0), (0, 50), 5))
    torso_body.position = x, y + 30
    torso_shape = pymunk.Segment(torso_body, (0, 0), (0, 50), 5)
    torso_shape.elasticity = 0.5
    space.add(torso_body, torso_shape)

    # Neck joint
    joint = pymunk.PinJoint(head_body, torso_body, (0, 15), (0, 0))
    space.add(joint)

    return [head_body, torso_body]

# stickman = create_stickman_old(space, 400, 100)

def create_stickman(space, x, y):
    bodies = []

    # Head
    head_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 15))
    head_body.position = x, y
    head_shape = pymunk.Circle(head_body, 15)
    head_shape.elasticity = 0.5
    space.add(head_body, head_shape)
    bodies.append(head_body)

    # Torso
    torso_body = pymunk.Body(2, pymunk.moment_for_segment(2, (0, 0), (0, 50), 5))
    torso_body.position = x, y + 30
    torso_shape = pymunk.Segment(torso_body, (0, 0), (0, 50), 5)
    torso_shape.elasticity = 0.5
    space.add(torso_body, torso_shape)
    bodies.append(torso_body)

    # Neck joint
    space.add(pymunk.PinJoint(head_body, torso_body, (0, 15), (0, 0)))

    # Arms (left and right)
    for dx in [-20, 20]:
        arm = pymunk.Body(1, pymunk.moment_for_segment(1, (0, 0), (0, 30), 3))
        arm.position = x + dx, y + 40
        arm_shape = pymunk.Segment(arm, (0, 0), (0, 30), 3)
        arm_shape.elasticity = 0.5
        space.add(arm, arm_shape)
        space.add(pymunk.PinJoint(torso_body, arm, (dx, 10), (0, 0)))
        bodies.append(arm)

    # Legs (left and right)
    for dx in [-10, 10]:
        leg = pymunk.Body(1, pymunk.moment_for_segment(1, (0, 0), (0, 40), 3))
        leg.position = x + dx, y + 80
        leg_shape = pymunk.Segment(leg, (0, 0), (0, 40), 3)
        leg_shape.elasticity = 0.5
        leg_shape.friction = 2.0 # Huh!?
        space.add(leg, leg_shape)
        space.add(pymunk.PinJoint(torso_body, leg, (dx, 50), (0, 0)))
        bodies.append(leg)

    # return bodies # Old return
    return {
        "bodies": bodies,
        "torso": torso_body
    }


stickman = create_stickman(space, 123, 100)
stickman = create_stickman(space, 400, 123)
stickman = create_stickman(space, 345, 100)
stickman = create_stickman(space, 400, 345)
stickman = create_stickman(space, 234, 100)
stickman2 = create_stickman(space, 700, 124)

# What?
# print(Fore.RED + stickman["torso"]) # not working
# print(Fore.RED + f"stickman: {stickman["torso"]}")
# stickman["torso"]
# help(torso.apply_impulse_at_local_point) # See if there's a docstring


# Old event
'''    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
'''

running = True
# This is my main event loop, correct?
while running:
    screen.fill((30, 30, 30))

    upright = pymunk.DampedRotarySpring(space.static_body, stickman["torso"], 0, 2000000, 100000)
    space.add(upright)


# The order is not a big deal? The indent is pretty important!
    if dragged_joint:
        mouse_pos = pygame.mouse.get_pos()
        mouse_point = pymunk.pygame_util.from_pygame(mouse_pos, screen)
        mouse_body.position = mouse_point

    # Keypress - Space logic
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        torso = stickman["torso"]
        torso.apply_impulse_at_local_point((0,-500)) # Jump

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            point = pymunk.pygame_util.from_pygame(pos, screen)
            shape = space.point_query_nearest(point, 5, pymunk.ShapeFilter())
            if shape:
                dragged_shape = shape.shape
                mouse_body.position = point
                dragged_joint = pymunk.PivotJoint(mouse_body, dragged_shape.body, (0, 0), dragged_shape.body.world_to_local(point))
                dragged_joint.max_force = 50000  # control "strength"
                space.add(dragged_joint)

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragged_joint:
                space.remove(dragged_joint)
                dragged_joint = None
                dragged_shape = None

    space.step(1/60.0)
    space.debug_draw(draw_options)
    pygame.display.flip()
    clock.tick(70) # Frames/tick






print("Winners never quit! Quitters never win!")
pygame.quit()