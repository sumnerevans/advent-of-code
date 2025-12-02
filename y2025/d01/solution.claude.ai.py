with open('01.txt', 'r') as f:
    lines = f.read().strip().split('\n')

position = 50
count = 0

for line in lines:
    direction = line[0]
    distance = int(line[1:])

    if direction == 'L':
        position = (position - distance) % 100
    else:  # R
        position = (position + distance) % 100

    if position == 0:
        count += 1

print(count)
