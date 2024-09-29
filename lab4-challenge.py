import random
import math

class MelodyGen:
    def __init__(self, initial_melody, target_phrases, grammar_rules, T0, alpha, max_iter):
        self.current_melody = initial_melody
        self.target_phrases = target_phrases
        self.grammar_rules = grammar_rules
        self.temperature = T0
        self.alpha = alpha
        self.max_iter = max_iter

    def cost(self, melody):
        cost = 0
        for phrase in self.target_phrases:
            if phrase in ' '.join(melody):
                cost -= 10
        return cost

    def modify(self, melody):
        new_melody = melody[:]
        idx1, idx2 = random.sample(range(len(new_melody)), 2)
        new_melody[idx1], new_melody[idx2] = new_melody[idx2], new_melody[idx1]
        return new_melody

    def anneal(self):
        initial_cost = self.cost(self.current_melody)
        for i in range(self.max_iter):
            new_melody = self.modify(self.current_melody)
            new_cost = self.cost(new_melody)
            delta_cost = new_cost - initial_cost
            if delta_cost < 0:
                self.current_melody = new_melody
                initial_cost = new_cost
            else:
                acceptance_prob = math.exp(-delta_cost / self.temperature)
                if random.random() < acceptance_prob:
                    self.current_melody = new_melody
                    initial_cost = new_cost
            self.temperature *= self.alpha
        return self.current_melody

initial_melody = ['Sa', 'Re', 'Ga', 'Ma', 'Pa', 'Dha', 'Ni', 'Sa']
target_phrases = ['Sa Re', 'Ga Ma Pa']
grammar_rules = []

T0 = 1000
alpha = 0.95
max_iter = 1000

melody_gen = MelodyGen(initial_melody, target_phrases, grammar_rules, T0, alpha, max_iter)
generated_melody = melody_gen.anneal()
print("Generated Melody:", generated_melody)
