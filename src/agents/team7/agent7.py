import numpy as np
import random

from utils.track_utils import compute_curvature, compute_slope
from agents.kart_agent import KartAgent

class Agent7(KartAgent):
    def __init__(self, env, path_lookahead=3):
        super().__init__(env)
        self.path_lookahead = path_lookahead
        self.agent_positions = []
        self.obs = None
        self.isEnd = False
        self.course = 0
        self.path_start = [-0.47596437,  0.09875359, -2.0172303 ] # position de la piste de course 
        self.name = "Ayse_koseoglu" # replace with your chosen name

    def reset(self):
        self.obs, _ = self.env.reset()
        self.agent_positions = []
        self.path_start

    def endOfTrack(self):
        return self.isEnd

    def choose_action(self, obs):
        acceleration = random.random()
    
        nodes_path = obs.get("paths_start", [])
        self.course+=1  # on compte le nombre de pas de temps 
        liste = []
        liste.append(nodes_path)
        # permet au kart d'aller au centre de la piste 
        # Calcul du steering vers le nœud cible
        if len(nodes_path) > self.path_lookahead:
            target_node = nodes_path[self.path_lookahead]
            angle_target = np.arctan2(target_node[0], target_node[2])
            steering = np.clip(angle_target * 2, -1, 1)
        else:
            steering = 0
        print(self.course)
        
        if self.course >= 200 : 
            # on prend la distance depuis le point de départ : 
            k = 1
            for i in (liste[:-1]):   
                target_node = i
                angle_target = np.arctan2(target_node[0], target_node[2])
                steering = np.clip(angle_target * 2, -1, 1)
        
                return    {
                "acceleration": acceleration,
                "steer": -(steering),
                "brake": 1,
                "drift": False,
                "nitro": False,
                "rescue":False,
                "fire": False,
            }
        else : 
        
            action = {
                "acceleration": acceleration,
                "steer": steering,
                "brake": False, # bool(random.getrandbits(1)),
                "drift": False,
                "nitro": False,
                "rescue":False,
                "fire": False,
        }
            return action
