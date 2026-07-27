import math

def get_distance(x1, y1, x2, y2):
    """
    Return the straight-line distance between two points.
    """

    return math.hypot(x2 - x1, y2 - y1)


def move_towards_position(enemy, target_x, target_y):
    """
    Move an enemy towards a target.
    
    Dead enemies remain at killed x,y location.
    """

    if enemy.health <= 0:
        return

    if enemy.x < target_x:
        enemy.x = min(enemy.x + enemy.speed, target_x)
    elif enemy.x > target_x:
        enemy.x = max(enemy.x - enemy.speed, target_x)

    if enemy.y < target_y:
        enemy.y = min(enemy.y + enemy.speed, target_y)
    elif enemy.y > target_y:
        enemy.y = max(enemy.y - enemy.speed, target_y)


def update_enemy_ai(enemy, target):
    """
    Update an enemy's behaviour based on its current state.
    """

    if enemy.health <= 0:
        return

    distance_to_target = get_distance(
        enemy.x,
        enemy.y,
        target.x,
        target.y,
    )

    if enemy.state == "idle":
        if distance_to_target <= enemy.detection_range:
            enemy.state = "chase"

    elif enemy.state == "chase":
        move_towards_position(
            enemy,
            target.x,
            target.y,
        )

        distance_from_spawn = get_distance(
            enemy.x,
            enemy.y,
            enemy.spawn_x,
            enemy.spawn_y,
        )

        if distance_from_spawn >= enemy.leash_range:
            enemy.state = "return"

    elif enemy.state == "return":
        move_towards_position(
            enemy,
            enemy.spawn_x,
            enemy.spawn_y,
        )

        if enemy.x == enemy.spawn_x and enemy.y == enemy.spawn_y:
            enemy.state = "idle"