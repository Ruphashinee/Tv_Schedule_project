import streamlit as st
import pandas as pd
import csv
import random

# ===================== READ CSV =======================
def read_csv_to_dict(file_path):
    program_ratings = {}
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            program = row[0]
            ratings = [float(x) for x in row[1:]]
            program_ratings[program] = ratings
    return program_ratings

file_path = "program_ratings.csv"
ratings = read_csv_to_dict(file_path)

# ===================== PARAMETERS =======================
GEN = 100
POP = 50
CO_R = 0.8
MUT_R = 0.2
EL_S = 2

all_programs = list(ratings.keys())
all_time_slots = list(range(6, 24))  # Hours 6–23

# ===================== FUNCTIONS =======================
def fitness_function(schedule):
    total_rating = 0
    for time_slot, program in enumerate(schedule):
        total_rating += ratings[program][time_slot]
    return total_rating

def crossover(schedule1, schedule2):
    crossover_point = random.randint(1, len(schedule1) - 2)
    child1 = schedule1[:crossover_point] + schedule2[crossover_point:]
    child2 = schedule2[:crossover_point] + schedule1[crossover_point:]
    return child1, child2

def mutate(schedule):
    mutation_point = random.randint(0, len(schedule) - 1)
    new_program = random.choice(all_programs)
    schedule[mutation_point] = new_program
    return schedule

def genetic_algorithm(initial_schedule, generations=GEN, population_size=POP, crossover_rate=CO_R, mutation_rate=MUT_R, elitism_size=EL_S):
    population = [initial_schedule]
    for _ in range(population_size - 1):
        random_schedule = initial_schedule.copy()
        random.shuffle(random_schedule)
        population.append(random_schedule)

    for _ in range(generations):
        population.sort(key=lambda s: fitness_function(s), reverse=True)
        new_population = population[:elitism_size]
        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population, k=2)
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()

            if random.random() < mutation_rate:
                child1 = mutate(child1)
            if random.random() < mutation_rate:
                child2 = mutate(child2)

            new_population.extend([child1, child2])
        population = new_population
    return population[0]

# ===================== STREAMLIT UI =======================
st.title("🎬 Optimal TV Program Scheduling using Genetic Algorithm")

st.write("This app finds the best program schedule (6 AM - 11 PM) based on audience ratings using a Genetic Algorithm.")

if st.button("Run Optimization"):
    initial_schedule = random.sample(all_programs, len(all_programs))
    best_schedule = genetic_algorithm(initial_schedule)

    total = fitness_function(best_schedule)

    st.subheader("🕒 Optimal Schedule")
    schedule_df = pd.DataFrame({
        "Hour": [f"{h:02d}:00" for h in all_time_slots],
        "Program": best_schedule
    })
    st.dataframe(schedule_df)

    st.success(f"✅ Total Rating Score: {total:.2f}")

else:
    st.info("Click 'Run Optimization' to generate the best schedule.")
