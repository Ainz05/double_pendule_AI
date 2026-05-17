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

    # Calcule des accélération à l'instant t des deux masses du pendule (dérivées des vitesses)
    # avec les équations de lagrange
    
    a1 = (m2 * L1 * omega1**2 * np.sin(theta2 - theta1) * np.cos(theta2 - theta1) + m2 * g * np.sin(theta2) * np.cos(theta2 - theta1) + m2 * L2 * omega2**2 * np.sin(theta2 - theta1) - (m1 + m2) * g * np.sin(theta1)) / (m1 + m2) * L1 - m2 * L1 * np.cos(theta2 - theta1) * np.cos(theta2 - theta1)
    a2 = (-m2 * L2 * omega2**2 * np.sin(theta2 - theta1) * np.cos(theta2 - theta1) + (m1 + m2) * g * np.sin(theta1) * np.cos(theta2- theta1) - (m1 + m2) * L1 * omega1**2 * np.sin(theta2 - theta1) - (m1 + m2) * g * np.sin(theta2)) / (L2 / L1) * (m1 + m2) * L1 - m2 * L1 * np.cos(theta2 - theta1) * np.cos(theta2 - theta1)
    


    
    