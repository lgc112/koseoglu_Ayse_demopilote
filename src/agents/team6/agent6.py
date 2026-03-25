import numpy as np
import random

from utils.track_utils import compute_curvature, compute_slope
from agents.kart_agent import KartAgent


class Agent6(KartAgent):
    def __init__(self, env, path_lookahead=3):
        super().__init__(env)
        self.path_lookahead = path_lookahead
        self.agent_positions = []
        self.obs = None
        self.isEnd = False
        self.name = "Ayse_Koseoglu" # on remplace le nom de team 6 par le notre 

    def reset(self):
        self.obs, _ = self.env.reset()
        self.agent_positions = []

    def endOfTrack(self):
        return self.isEnd

    def choose_action(self, obs):
        steering = 1
        # partie de l exo1 pour faire simplement un tour complet 
        if obs is not None : # tou d'abord on verifie que le dictionnaire observation n est pas vide 
            phase = obs.get("phase") # on prend la phase qui nous permet de savoir qaund est ce que la course a commencé 
            speed = obs.get("velocity") # on prend les coordonnées du vecteur vitesse de notre kart
            vitesse = np.linalg.norm(speed) # on prend la norme de ces coordonnées 
            if vitesse < 0.2 and phase > 2 :  # si la vitesse est inférieure à 0.2  alors on braque et on evite l 'obstacle 
                return {
                "acceleration": 0.0,
                "steer": -0.9 if steering > 0 else 0.8 ,
                "brake": True,   # brake=True active la marche arrière dans STK
                "drift": False,
                "nitro": False,
                "rescue": False,
                "fire": False,
            }
        
        acceleration = random.random()
        action = {
            "acceleration": acceleration,
            "steer": steering,
            "brake": False, # bool(random.getrandbits(1)),
            "drift": bool(random.getrandbits(1)),
            "nitro": bool(random.getrandbits(1)),
            "rescue":bool(random.getrandbits(1)),
            "fire": bool(random.getrandbits(1)),
        }
        return action
