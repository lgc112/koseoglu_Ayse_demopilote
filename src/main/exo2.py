"""
MultiAgent race

All initial agents are RandomAgent
The simulation runs on the "black_forest" track with MAX_TEAMS karts.
"""

import sys, os
import numpy as np
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass


# Append the "src" folder to sys.path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))


from agents.team7.agent7 import Agent7
from pystk2_gymnasium.envs import STKRaceMultiEnv, AgentSpec
from pystk2_gymnasium.definitions import CameraMode

MAX_TEAMS = 7
MAX_STEPS = 1000 # on modifie le nombre de pas de temps non pas a 1000 mais 200
# je vais mettre a 1000 pour l exercice 2B. pour voir si ca fonctionne bien 
NB_RACES = 1

# Get the current timestamp
current_timestamp = datetime.now()

# Format it into a human-readable string
formatted_timestamp = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")

@dataclass
class Scores:
    def __init__(self):
        self.dict = {}
    
    def init(self, name):
        self.dict[name] = [[], [], [], []]

    def append(self, name, pos, pos_std, dist, dist_std):
        self.dict[name][0].append(pos)
        self.dict[name][1].append(pos_std)
        self.dict[name][2].append(dist)
        self.dict[name][3].append(dist_std)

    def display(self):
        print(self.dict)

    def display_mean(self):
        for k in self.dict:
            print(f"{k}: {np.array(self.dict[k][0]).mean()}, {np.array(self.dict[k][1]).mean()}, {np.array(self.dict[k][2]).mean()}, {np.array(self.dict[k][3]).mean()}")

    def display_html(self, fp):
        for k in self.dict:
            fp.write(f"""<tr><td>{k}</td>""")
            fp.write(
                    f"""<td>{np.array(self.dict[k][0]).mean():.2f}</td>"""
                    f"""<td>{np.array(self.dict[k][1]).mean():.2f}</td>"""
                    f"""<td>{np.array(self.dict[k][2]).mean():.2f}</td>"""
                    f"""<td>{np.array(self.dict[k][3]).mean():.2f}</td>"""
                    "</tr>"
                )
            

default_action = {
            "acceleration": 0.0,
            "steer": 0.0,
            "brake": False, # bool(random.getrandbits(1)),
            "drift": False, # bool(random.getrandbits(1)),
            "nitro": False, # bool(random.getrandbits(1)),
            "rescue":False, # bool(random.getrandbits(1)),
            "fire": False, # bool(random.getrandbits(1)),
        }


# Make AgentSpec hashable.
def agent_spec_hash(self):
    return hash((self.name, self.rank_start, self.use_ai, self.camera_mode))
AgentSpec.__hash__ = agent_spec_hash

# Create agents specifications.
agents_specs = [
    # on enleve la boucle pour n'avoir qu'a l'écran le kart de la team 7
    AgentSpec(name=f"Team{7}", rank_start=1, use_ai=False, camera_mode=CameraMode.ON) 
]

def create_race():
    # Create the multi-agent environment for N karts.
    if NB_RACES==1:
        env = STKRaceMultiEnv(agents=agents_specs, track="abyss", render_mode="human", num_kart=MAX_TEAMS)
    else:
        env = STKRaceMultiEnv(agents=agents_specs, render_mode="human", num_kart=MAX_TEAMS)

    # Instantiate the agents.

    agents = []
    names = []

    #agents.append(Agent1(env, path_lookahead=3))
    #agents.append(Agent2(env, path_lookahead=3))
    #agents.append(Agent3(env, path_lookahead=3))
    #agents.append(Agent4(env, path_lookahead=3))
    #agents.append(Agent5(env, path_lookahead=3))
    #agents.append(Agent6(env, path_lookahead=3))
    agents.append(Agent7(env, path_lookahead=3))
    np.random.shuffle(agents)

    
    names.append(agents[0].name)
    agents_specs[0].name = agents[0].name
    agents_specs[0].kart = agents[0].name
    return env, agents, names


def single_race(env, agents, names, scores):
    obs, _ = env.reset()
    done = False
    steps = 0
    nb_finished = 0
    positions = []
    distances = []
    while not done and steps < MAX_STEPS:
        actions = {}
        env.world_update()
        
        str = f"{0}"
        try:
            actions[str] = agents[0].choose_action(obs[str])
        except Exception as e:
            print(f"Team {7} error: {e}")
            actions[str] = default_action

            # check if agents have finished the race
        kart = env.world.karts[0]
        if kart.has_finished_race and not agents[0].isEnd:
            print(f"{names[0]} has finished race !")
            nb_finished += 1
            agents[0].isEnd = True

        obs, _, _, _, info = env.step(actions)

        # prepare data to display leaderboard
        pos = np.zeros(1)
        dist = np.zeros(1)
        
        str = f"{0}"
        pos[0] = info['infos'][str]['position']
        dist[0] = info['infos'][str]['distance']
        steps = steps + 1
        done = (nb_finished == 5)
        positions.append(pos)
        distances.append(dist)
    pos_avg = np.array(positions).mean(axis=0)
    pos_std = np.array(positions).std(axis=0)
    dist_avg = np.array(distances).mean(axis=0)
    dist_std = np.array(distances).std(axis=0)

    scores.append(names[0], pos_avg[0], pos_std[0], dist_avg[0], dist_std[0])
    agents[0].isEnd = False
    print("race duration:", steps)

def main_loop():
    scores = Scores()
    #unsatisfactory: first call just to init the names
    env, agents, names = create_race()

    scores.init(names[0])

    for j in range(NB_RACES):
        print(f"race : {j}")
        env, agents, names = create_race()
        single_race(env, agents, names, scores)

        env.close()

    print("final scores:")
    return scores


def output_html(output: Path, scores: Scores):
    # Use https://github.com/tofsjonas/sortable?tab=readme-ov-file#1-link-to-jsdelivr
    with output.open("wt") as fp:
        fp.write(
            f"""<html><head>
<title>STK Race results</title>
<link href="https://cdn.jsdelivr.net/gh/tofsjonas/sortable@latest/dist/sortable.min.css" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/gh/tofsjonas/sortable@latest/dist/sortable.min.js"></script>
<body>
<h1>Team evaluation on SuperTuxKart</h1><div style="margin: 10px; font-weight: bold">Timestamp: {formatted_timestamp}</div>
<table class="sortable n-last asc">
  <thead>
    <tr>
      <th class="no-sort">Name</th>
      <th id="position">Avg. position</th>
      <th class="no-sort">±</th>
      <th id="position">Avg. distance</th>
      <th class="no-sort">±</th>
    </tr>
  </thead>
  <tbody>"""
        )

        scores.display_html(fp)
            
        fp.write(
            """<script>
  window.addEventListener('load', function () {
    const el = document.getElementById('position')
    if (el) {
      el.click()
    }
  })
</script>
"""
        )
        fp.write("""</body>""")

if __name__ == "__main__":
    scores = main_loop()
    output_html(Path("../../docs/index.html"), scores)
