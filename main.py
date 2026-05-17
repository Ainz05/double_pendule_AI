import numpy as np
import cv2
from scipy.integrate import odeint

# Constante du pendule
L1 = 1.0
L2 = 1.0
m1 = 1.0
m2 = 1.0
g = 9.81
afficher = False
save = True

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
    
    return [omega1, omega2, a1, a2]
    
def draw_pendule(theta1, theta2):
    
    # Dessiner le fond (en noire pour faciliter l'entrainement du modèle)
    image = np.zeros((64,64), dtype=np.uint8) # uint8 signifie qu'on utilise des nombres entre 0 et 255 pour représenter les niveaux de gris

    center_x, center_y = 32, 32

    # Mise à l'échelle pour que les longueurs s'adaptent à l'image
    echelle = 15
    
    # Positions des masses (dépend des angles) en mètres
    x1 = L1 * np.sin(theta1)
    y1 = L1 * np.cos(theta1)

    x2 = x1 + L2 * np.sin(theta2)
    y2 = y1 + L2 * np.cos(theta2)

    # Conversion en pixels pour l'affichage (int() car un pixel non entier n'existe pas)
    x1_pixel = center_x + int(x1 * echelle)
    y1_pixel = center_y + int(y1 * echelle)

    x2_pixel = center_x + int(x2 * echelle)
    y2_pixel = center_y + int(y2 * echelle)

    # ligne entre les différentes masses
    cv2.line(image, (center_x, center_y), (x1_pixel, y1_pixel), 255, 1)
    cv2.line(image, (x1_pixel, y1_pixel), (x2_pixel, y2_pixel), 255, 1)

    # Points des masses (3 pixels)
    cv2.circle(image, (x1_pixel, y1_pixel), 2, 255, -1)
    cv2.circle(image, (x2_pixel, y2_pixel), 2, 255, -1)

    return image

def generer_dataset(nb_videos=10, fps=30, duree=3):
    frames_par_video = fps * duree
    t = np.linspace(0, duree, frames_par_video)
    
    # Création d'un tenseur vide pour stocker TOUTES les vidéos
    # Dimensions : (Nombre de vidéos, Temps, Hauteur, Largeur, Canaux)
    # Le '1' à la fin indique qu'il y a 1 seul canal de couleur (Niveaux de gris)
    dataset = np.zeros((nb_videos, frames_par_video, 64, 64, 1), dtype=np.uint8)
    
    print(f"Génération de {nb_videos} vidéos en cours...")
    
    for i in range(nb_videos):

        th1_init = np.random.uniform(-np.pi, np.pi)
        th2_init = np.random.uniform(-np.pi, np.pi)
        etat_initial = [th1_init, 0.0, th2_init, 0.0] # Vitesses initiales = 0
        
        # Résolution de l'équation différentielle pour toute la durée
        solution = odeint(calculate_derivates, etat_initial, t)
        
        # Transformation de la solution mathématique en vidéo
        for frame_idx, etat in enumerate(solution):
            img = draw_pendule(etat[0], etat[2])
            dataset[i, frame_idx, :, :, 0] = img

            # Affichage de l'image
            if afficher == True:
                img_agrandie = cv2.resize(img, (512, 512), interpolation=cv2.INTER_NEAREST)
                cv2.imshow("Simulation Double Pendule", img_agrandie)
                if cv2.waitKey(33) & 0xFF == ord('q'):
                    break
            
        if (i + 1) % 50 == 0 or (i + 1) == nb_videos:
            print(f"Progression : {i + 1} / {nb_videos}")

    # Sauvegarde des données
    if save == True:
        nom_fichier = "pendule_dataset.npy"
        np.save(nom_fichier, dataset)
        print(f"Terminé ! Fichier '{nom_fichier}' sauvegardé (Taille estimée : {dataset.nbytes / 1e6:.2f} Mo)")
    else:
        print("Les données ont été générées mais non sauvegardées.")

    cv2.destroyAllWindows() 

if __name__ == "__main__":
    # Pour tester, on génère 10 vidéos
    generer_dataset(nb_videos=10, fps=30, duree=3)