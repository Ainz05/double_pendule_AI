import numpy as np


# Constante du pendule
L1 = 1.0
L2 = 1.0
m1 = 1.0
m2 = 1.0
g = 9.81

def calculate_derivates(etat, t):

    # Données de l'état actuel du pendule
    theta1, theta2, omega1, omega2 = etat

    # Simplifie les calculs, rend le code plus lisible
    delta = theta2 - theta1

    den1 = (m1 + m2) * L1 - m2 * L1 * np.cos(delta) * np.cos(delta)
    den2 = (L2 / L1) * den1
    
    # Calcule des accélération à l'instant t des deux masses du pendule (dérivées des vitesses)
    # avec les équations de lagrange
    
    a1 = (m2 * L1 * omega1**2 * np.sin(delta) * np.cos(delta) + m2 * g * np.sin(theta2) * np.cos(delta) + m2 * L2 * omega2**2 * np.sin(delta) - (m1 + m2) * g * np.sin(theta1)) / den1
    a2 = (-m2 * L2 * omega2**2 * np.sin(delta) * np.cos(delta) + (m1 + m2) * g * np.sin(theta1) * np.cos(delta) - (m1 + m2) * L1 * omega1**2 * np.sin(delta) - (m1 + m2) * g * np.sin(theta2)) / den2
    

    
    