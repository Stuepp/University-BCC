class Item:
    def __init__(self):
        self.vals = []
        self.group = 0

ITENS = []

f = open('dados.txt', 'r')

for x in f:
    item =  Item()
    fields = x.split(';')
    item.vals.append(float(fields[0]))
    item.vals.append(float(fields[1]))
    item.group = float(fields[2])
    ITENS.append(item)
f.close()

for i in ITENS:
    print(i.vals, i.group)
