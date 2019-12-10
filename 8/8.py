def choose(upper_layer, lower_layer):
    if (upper_layer == 2):
        return lower_layer
    else:
        return upper_layer

with open("input.txt") as f:
    image_data = f.read()
    width = 25
    height = 6
    size = width*height
    i = 0
    min_zeroes = width*height
    twos = 0
    ones = 0
    while((i+1)*size < len(image_data)):
        start = i*size
        end = (i+1)*size
        layer = str(image_data[start:end])
        layer_zeroes = layer.count('0')
        min_zeroes = min(min_zeroes, layer_zeroes)
        if min_zeroes == layer_zeroes:
            twos = layer.count('2')
            ones = layer.count('1')
        i += 1

    print('Part1: {}'.format(ones*twos))

    layers = int(len(image_data) / (size))
    image = [2] * size
    i = 0
    while((i+1)*size < len(image_data)):
        start = i*size
        end = (i+1)*size
        layer = str(image_data[start:end])
        for idx, digit in enumerate(layer):
            image[idx] = choose(image[idx], int(digit))
        i += 1

    for h in range(height):
        print(str(image[h*width:(h+1)*width]).replace('1', '#').replace('0', '.'))
