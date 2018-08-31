	if player_car.x >= 227 and keys[key.LEFT]:
        player_car.x -= player_car.dx * dt
    if player_car.x <= 773 and keys[key.RIGHT]:
        player_car.x += player_car.dx * dt
    if player_car.y >= 93 and keys[key.DOWN]:
        player_car.y -= player_car.dx * dt
    if player_car.y <= 860 and keys[key.UP]:
        player_car.y += player_car.dx * dt