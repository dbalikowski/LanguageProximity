import areSimilar as sim

word_1A = "pear"
word_1B = "pera"

word_2A = "mama"
word_2B = "mutter"

# example 1
print(sim.areSimilar(word_1A,word_1B))

# example 2
print(sim.areSimilar(word_2A,word_2B))
print(sim.areSimilar(word_2A,word_2B,0.1))