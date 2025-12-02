with open('01.txt', 'r') as f:
    lines = f.read().strip().split('\n')

position = 50
count = 0

for line in lines:
    direction = line[0]
    distance = int(line[1:])

    if direction == 'L':
        # Left rotation
        if position == 0:
            count += distance // 100
        else:
            if distance >= position:
                count += 1 + (distance - position) // 100
    else:  # R
        # Right rotation
        count += (position + distance) // 100

    # Update position
    if direction == 'L':
        position = (position - distance) % 100
    else:
        position = (position + distance) % 100

print(count)
