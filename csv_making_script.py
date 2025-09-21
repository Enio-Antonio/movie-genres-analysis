data = open("datasetfilmes.txt")

dataset = open("dataset.csv", 'w')
dataset.write("id,titulo,renda,publico,renda_total,publico_total,salas,distribuidora,estreia")
dataset.write("\n")
counter = 0

for word in data.read().split("\n"):
    if counter < 8:
        dataset.write(word)
        dataset.write(',')
        counter += 1
    else:
        dataset.write("\n")
        counter = 0

data.close()
dataset.close()