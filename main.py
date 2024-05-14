from PIL import Image

size = 1000
scale = 0.3
posx = 0
posy = 0
max_iterations = 100

im = Image.new("RGB", (size, size), (0, 0, 0))

for x in range(size):
    for y in range(size):
        c = scale * complex(x - size/2 + posx * size / scale, size/2 - y + posy * size / scale) / (size / 10)
        if abs(c) > 2:
            continue

        z = 0
        stable = True
        iteration = 0
        for i in range(max_iterations):
            z = z ** 2 + c
            if abs(z) > 2:
                iteration = int(i / max_iterations * 255)
                stable = False
                break

        if not stable:
            im.putpixel((x, y), (0, iteration, 0))

im.save("test.png")
im.show()
