f=open("gyongyok.txt")
lines=f.readlines()
f.close()
max_x=0
max_y=0
max_z=0
max_e=0
for id,line in enumerate(lines):
    if id==0:
        continue
    parts=line.strip().split(";")
    if int(parts[0])>max_x:
        max_x=int(parts[0])
    if int(parts[1])>max_y:
        max_y=int(parts[1])
    if int(parts[2])>max_z:
        max_z=int(parts[2])
    if int(parts[3])>max_e:
        max_e=int(parts[3])
print(max_x)
print(max_y)
print(max_z)
print(max_e)