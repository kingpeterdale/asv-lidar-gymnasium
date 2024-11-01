import gymnasium
from asv_lidar_gymnasium.envs.asv_lidar_gym import ASVLidarEnv, CENTER, PORT, STBD

gymnasium.register(
    id="ASVLidar-v0",
    entry_point="asv_lidar_gymnasium:ASVLidarEnv"
)