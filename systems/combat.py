def player_attack(player, enemy, current_time, colliding):
    if not colliding:
        return

    if player.health <= 0 or enemy.health <= 0:
        return

    if current_time - player.last_attack_time < player.attack_cooldown:
        return

    damage = player.final_stats["damage"]
    enemy.health = max(0, enemy.health - damage)
    player.last_attack_time = current_time

    print(f"Player hits {enemy.__class__.__name__} for {damage} damage!")

def enemy_attack(enemy, player, current_time, colliding):
    if not colliding:
        return

    if enemy.health <= 0 or player.health <= 0:
        return

    if current_time - enemy.last_attack_time < enemy.attack_cooldown:
            return

    damage = round(enemy.damage * (1 - player.defence_percent))
    player.health = max(0, player.health - damage)
    enemy.last_attack_time = current_time

    print(f"{enemy.__class__.__name__} hits player for {damage} damage!")