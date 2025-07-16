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
# floor.friction = 1.0 # WTF friction not working?
space.add(floor)

def create_stickman(space, x, y, color=(0,0,0)):
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
        "torso": torso_body,
        "player_color": color
    }, color

stickmen = []
stickman1, color1 = create_stickman(space, 123, 100,(0,0,255))
stickmen.append((stickman1, color1))

stickman2, color2 = create_stickman(space, 700, 124,(0,255,00))
stickmen.append((stickman2, color2))

BadGuy_stickman_NPC1, color3 = create_stickman(space, 400, 123,(255,0,0))
BadGuy_stickman_NPC2, color4 = create_stickman(space, 123, 400,(255,0,0))
stickmen.append((BadGuy_stickman_NPC1, color3))
stickmen.append((BadGuy_stickman_NPC2, color4))


screen.fill((255, 255, 255))  # Clear screen (white background)

print("HEY!!!!!!!")
# Use Color
for shapes, color in stickmen:
    print("HELLO!#!#?") 
    for shape in shapes:
        if isinstance(shape, pymunk.Segment):
            body = shape.body
            a = body.position + shape.a.rotated(body.angle)
            b = body.position + shape.b.rotated(body.angle)
            print(color)
            print("HELLO?") # I don't get inside this part?
            pygame.draw.line(screen, color, a, b, int(shape.radius * 2))
        elif isinstance(shape, pymunk.Circle):
            pos = int(shape.body.position.x), int(shape.body.position.y)
            pygame.draw.circle(screen, color, pos, int(shape.radius))


# help(torso.apply_impulse_at_local_point) # See if there's a docstring
upright = pymunk.DampedRotarySpring(space.static_body, stickman1["torso"], 0, 2000000, 100000)
space.add(upright)

running = True
# This is my main event loop, correct?
while running:
    screen.fill((30, 30, 30))

# The order is not a big deal? The indent is pretty important!
    if dragged_joint:
        mouse_pos = pygame.mouse.get_pos()
        mouse_point = pymunk.pygame_util.from_pygame(mouse_pos, screen)
        mouse_body.position = mouse_point

    # Keypress - Space logic - Jump
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        torso = stickman1["torso"]
        torso.apply_impulse_at_local_point((0,-500))

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