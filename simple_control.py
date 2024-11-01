import gymnasium as gym
from asv_lidar_gymnasium import CENTER, PORT, STBD
def run():

    env = gym.make("ASVLidar-v0")
    env.reset()

    running = True
    action = CENTER
    total_reward = 0
    while running:
        obs,rew,term,_,info = env.step(action)
        total_reward += rew
        if term:
            running = False

        hdg_sp = 0
        if obs['tgt'] > 4:
            hdg_sp = 25
        elif obs['tgt'] < -4:
            hdg_sp = -25
        
        action = CENTER
        if obs['hdg'] < hdg_sp:
            action = STBD
        elif obs['hdg'] >  hdg_sp:
            action = PORT

    print(f"Total Reward: {total_reward}")

if __name__ == '__main__':
    run()