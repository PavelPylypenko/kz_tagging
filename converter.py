with open('temp.txt') as file:
    text = file.read()
words = []
text = text.split(',')
for w in text:
    words.append(w.strip())

print(tuple(words))
