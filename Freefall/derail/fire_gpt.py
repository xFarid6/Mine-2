# Import the necessary libraries
import pygame
import numpy as np

# Define the size of the grid
grid_width = 100
grid_height = 100

# Initialize Pygame
pygame.init()

# Create the Pygame window
screen = pygame.display.set_mode((grid_width, grid_height))

# Create an array to represent the grid
grid = np.zeros((grid_width, grid_height))

# Define the number of particles
num_particles = 1000

# Create a list to store the particles
# Each element in the list will be a tuple containing the position and "on fire" state of a particle
particles = []

# Initialize the particles with random positions
for i in range(num_particles):
    particles.append((np.random.randint(0, grid_width), np.random.randint(0, grid_height), 0))

# Define the movement rules for the particles
# (e.g. how they are affected by wind, etc.)
def move_particles():
    for particle in particles:
        # Update the position of the particle based on its velocity
        particle[0] += np.random.normal(0, 0.1)
        particle[1] += np.random.normal(0, 0.1)

        # Make sure the particle stays within the bounds of the grid
        particle[0] = np.clip(particle[0], 0, grid_width-1)
        particle[1] = np.clip(particle[1], 0, grid_height-1)

# Define the rules for how the particles ignite and extinguish
# other objects in the environment
def update_fire():
    for particle in particles:
        # If the particle is on fire, set the grid cell it is in to "on fire"
        if particle[2] == 1:
            grid[int(particle[0]), int(particle[1])] = 1

        # If the particle is not on fire, but is in a cell that is on fire,
        # set the particle to "on fire" with some probability
        elif grid[int(particle[0]), int(particle[1])] == 1:
            if np.random.rand() < 0.01:
                particle[2] = 1

# Main simulation loop
while True:
    # Move the particles
    move_particles()

    # Update the fire
    update_fire()

    # Draw the grid on the Pygame window
    for i in range(grid_width):
        for j in range(grid_height):
            if grid[i, j] == 1:
                pygame.draw.rect(screen, (255, 0, 0), (i, j, 1, 1))

    # Update the Pygame window
    pygame.display.flip()
   
