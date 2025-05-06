import pygame, random, math, time
from Environment.env_1 import Env1
from Environment.env_2 import Env2
import numpy as np
from matplotlib import pyplot as plt

# Genetic Algorithm Constants
NO_OF_GENERATIONS = 10
RUNS_PER_GENERATION = 5
MUTATION_RATE = 0.2
WEIGHT_RANGE = (0.1, 2.0)

def random_genome(weight_range = WEIGHT_RANGE):
    return [random.uniform(*weight_range) for _ in range(3)]

def crossover(best_genomes):
    offspring = []
    for i in range(len(best_genomes)):
        for j in range(i + 1, len(best_genomes)):
            parent1 = best_genomes[i]
            parent2 = best_genomes[j]
            child1 = [parent1[0], parent2[1], parent1[2]]
            child2 = [parent2[0], parent1[1], parent2[2]]
            offspring.extend([child1, child2])
    return offspring[:8]


best_genome_per_generation = []
best_fitness_per_generation = []
average_fitness_per_generation = []

for i in range(NO_OF_GENERATIONS):
    genome_list = []
    fitness = []
    for j in range(RUNS_PER_GENERATION):
        pygame.init()
        WIDTH, HEIGHT = 1400, 1000
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Boids with GA")
        clock  = pygame.time.Clock()
        
        env = Env2(WIDTH, HEIGHT)
        env.populate_environment()
        env.create_target()
            
        if i < 1:
            w_align, w_coh, w_sep = random_genome()
        else:
            top_genomes = best_genome_per_generation[-1][:3]  
            offspring = crossover(top_genomes)
            w_align, w_coh, w_sep = offspring[j % len(offspring)]
        
        # Set Random Weights
        for b in env.birds:
            b.w_align = w_align
            b.w_coh = w_coh
            b.w_sep = w_sep

        
        genome_list.append([w_align, w_coh, w_sep])

        time_list = [] # Time to target
        target_pos = [] # Position of target
        target_pos.append(env.targets[0][0])

        running = True
        start_time = time.time()
        duration_limit = 20
        max_time = start_time + duration_limit
        time_for_target = pygame.time.get_ticks()
        while running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                    
            env.update_birds_in_target()
            if env.check_birds_in_target() == True:
                time_list.append(pygame.time.get_ticks() - time_for_target)
                time_for_target = pygame.time.get_ticks()
                env.clear_targets()
                env.clear_birds_target()
                env.create_target()
                target_pos.append(env.targets[0][0])
                
            if time.time() > max_time:
                distances = [np.linalg.norm(np.array(target_pos[i]) - np.array(target_pos[i-1])) for i in range(1, len(target_pos))]
                speeds = [distances[i] / time_list[i] for i in range(len(distances))]
                avg_speed = sum(speeds) / len (speeds)
                fitness.append(avg_speed)
                running = False
                
            env.update()
            env.render()
                
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
        
        print(f'Genome: {genome_list[j]}\nFitness: {fitness[j]}\n')


    sorted_genomes_and_fitness = sorted(zip(fitness, genome_list), key=lambda x: x[0], reverse=True)
    fitness, genome_list = zip(*sorted_genomes_and_fitness)
    
    best_fitness_per_generation.append(fitness[0])
    average_fitness_per_generation.append(sum(fitness) / len(fitness))
    best_genome_per_generation.append(genome_list[:3])


for generation in range(NO_OF_GENERATIONS):
    print(f"Generation {generation + 1}:")
    print(f"  Best Fitness: {best_fitness_per_generation[generation]}")
    print(f"  Best Genome: {best_genome_per_generation[generation]}")

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(range(1, NO_OF_GENERATIONS + 1), best_fitness_per_generation, label="Best Fitness", marker='o')
plt.plot(range(1, NO_OF_GENERATIONS + 1), average_fitness_per_generation, label="Average Fitness", marker='x')
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.title("Best and Average Fitness per Generation")
plt.legend()
plt.grid()
plt.show()