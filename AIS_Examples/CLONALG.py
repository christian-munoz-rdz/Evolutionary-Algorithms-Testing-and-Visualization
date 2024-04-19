import numpy as np
import matplotlib.pyplot as plt

# Función objetivo
def objective_function(x):
    return x**2 - 10*x + 25

# Generar población inicial
def generate_initial_population(size, x_bounds):
    return np.random.uniform(x_bounds[0], x_bounds[1], size)

# Clonar los mejores individuos
def clone(antibodies, n_clones):
    clones = []
    for antibody in antibodies:
        for _ in range(n_clones):
            clones.append(antibody)
    return clones

# Mutación de los clones
def mutate(clones, mutation_rate, x_bounds):
    mutated = []
    for clone in clones:
        if np.random.rand() < mutation_rate:
            mutation = np.random.normal(0, 1)
            mutated_clone = clone + mutation
            # Asegurar que el clon mutado esté dentro de los límites
            mutated_clone = np.clip(mutated_clone, x_bounds[0], x_bounds[1])
            mutated.append(mutated_clone)
        else:
            mutated.append(clone)
    return mutated

# Algoritmo de Selección Clonal
def clonal_selection(x_bounds, population_size, n_clones, mutation_rate, n_generations):
    population = generate_initial_population(population_size, x_bounds)
    best_solution = None
    best_fitness = float('inf')
    
    fitness_history = []
    
    for _ in range(n_generations):
        fitness = np.array([objective_function(ind) for ind in population])
        best_idx = np.argmin(fitness)
        if fitness[best_idx] < best_fitness:
            best_fitness = fitness[best_idx]
            best_solution = population[best_idx]
        
        # Selección de los mejores para clonación
        sorted_indices = np.argsort(fitness)
        best_individuals = population[sorted_indices[:2]]  # Tomar los 2 mejores
        clones = clone(best_individuals, n_clones)
        
        # Mutación
        mutated_clones = mutate(clones, mutation_rate, x_bounds)
        
        # Reemplazo
        population = np.concatenate([best_individuals, mutated_clones])
        
        fitness_history.append(best_fitness)
    
    return best_solution, fitness_history

# Parámetros del algoritmo
x_bounds = [-10, 20]
population_size = 10
n_clones = 5
mutation_rate = 0.4
n_generations = 50

best_solution, fitness_history = clonal_selection(x_bounds, population_size, n_clones, mutation_rate, n_generations)

# Gráfica de la función objetivo
x_values = np.linspace(x_bounds[0], x_bounds[1], 400)
y_values = objective_function(x_values)
plt.plot(x_values, y_values, label='f(x) = x^2 - 10x + 25')

# Marcar la mejor solución encontrada
plt.scatter([best_solution], [objective_function(best_solution)], color='red', label='Mejor solución')
plt.title('Optimización de f(x) usando Selección Clonal')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.show()

print("Mejor solución encontrada: x =", best_solution)
print("Valor de la función en la mejor solución: f(x) =", objective_function(best_solution))