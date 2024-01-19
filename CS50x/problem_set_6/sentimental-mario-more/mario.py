# mario more
height = 0
while height <= 0 or height >=23:
    height = int(input("Height:"))
spaces = height
hashtags = 0
for i in range(height):
    spaces -=1
    hashtags += 1
    print(" "*spaces+"#"*hashtags+"  "+"#"*hashtags+" "*spaces)