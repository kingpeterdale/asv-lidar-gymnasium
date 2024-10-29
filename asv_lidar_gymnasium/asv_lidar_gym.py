import gymnasium as gym
from gymnasium.spaces import Dict, Box, Discrete
import numpy as np
import pygame
import pygame.freetype
from ship_model import ShipModel
from asv_lidar import Lidar, LIDAR_RANGE, LIDAR_BEAMS

UPDATE_RATE = 0.1
RENDER_FPS = 60

# Actions
PORT = 0
CENTER = 1
STBD = 2
rudder_action = {
    PORT: -75,
    CENTER: 0,
    STBD: 75
}

class ASVLidarEnv(gym.Env):
    """ Autonomous Surface Vessel w/ LIDAR Gymnasium environment

        Args:
            render_mode (str): If/How to render the environment
                "human" will render a pygame windows, episodes are run in real-time
                None will not render, episodes run as fast as possible
    """
    
    metadata = {"render_modes": ["human"]}

    def __init__(
            self, 
            render_mode:str = 'human'
            ) -> None:
        
        pygame.init()
        self.render_mode = render_mode
        self.screen_size = (400,600)

        self.icon = None
        self.fps_clock = pygame.time.Clock()

        self.display = None
        self.surface = None
        self.status = None
        if render_mode in self.metadata['render_modes']:
            self.surface = pygame.Surface(self.screen_size)
            self.status = pygame.freetype.SysFont(pygame.font.get_default_font(),size=10)
        # State
        self.elapsed_time = 0.
        self.tgt_x = 0
        self.tgt_y = 0
        self.tgt = 0
        self.asv_y = 0
        self.asv_x = 0
        self.asv_h = 0
        self.asv_w = 0

        self.model = ShipModel()
        self.model._v = 4.5

        self.observation_space = Dict(
            {
                "lidar": Box(low=0,high=LIDAR_RANGE,shape=(LIDAR_BEAMS,),dtype=np.int16),
                "pos"  : Box(low=np.array([0,0]),high=np.array(self.screen_size),shape=(2,),dtype=np.int16),
                "hdg"  : Box(low=0,high=360,shape=(1,),dtype=np.int16),
                "dhdg" : Box(low=0,high=36,shape=(1,),dtype=np.int16),
                "tgt"  : Box(low=-50,high=50,shape=(1,),dtype=np.int16)
            }
        )
        self.action_space = Discrete(3)
        
        # LIDAR
        self.lidar = Lidar()


    def _get_obs(self):
        return {
            'lidar': self.lidar.ranges,
            'pos': [self.asv_x, self.asv_y],
            'hdg': [self.asv_h],
            'dhdg': [self.asv_w],
            'tgt': [self.tgt]
        }


    def reset(self):
        self.tgt_x = 150
        self.asv_y = 550
        self.asv_x = 200
        if self.render_mode in self.metadata['render_modes']:
            self.render()
        return self._get_obs()


    def step(self, action):
        self.elapsed_time += UPDATE_RATE
        dx,dy,h,w = self.model.update(100,rudder_action[action],UPDATE_RATE)#pygame.time.get_ticks() / 1000.)
        self.asv_x += dx
        self.asv_y -= dy
        self.asv_h = h
        self.asv_w = w
        self.tgt_y = self.asv_y-50
        self.tgt = self.tgt_x - self.asv_x

        self.lidar.scan((self.asv_x, self.asv_y),self.asv_h)

        if self.render_mode in self.metadata['render_modes']:
            self.render()

        # step loss
        reward = -1
        if self.tgt < 10 and self.tgt > -10:
            # on or near line
            reward = 0
        if dy < 0:
            # moving in reverse
            reward = -10
        terminated = (self.asv_y <= 0)
        return self._get_obs(), reward, terminated, False


    def render(self):
        if self.render_mode != 'human':
            return        
        if self.display is None:
            self.display = pygame.display.set_mode(self.screen_size)
        self.surface.fill((0, 0, 0))
        # Draw LIDAR scan
        self.lidar.render(self.surface)
        # Draw Path
        pygame.draw.line(self.surface,(0,200,0),(self.tgt_x,0),(self.tgt_x,self.screen_size[1]),5)
        pygame.draw.circle(self.surface,(100,0,0),(self.tgt_x,self.tgt_y),5)
        # Draw ownship
        if self.icon is None:
            self.icon = pygame.image.load('boat_icon.png').convert_alpha()
        # Draw status
        if self.status is not None:
            status, rect = self.status.render(f"{self.elapsed_time:005.1f}s  HDG:{self.asv_h:+004.0f}({self.asv_w:+03.0f})  TGT:{self.tgt:+004.0f}",(255,255,255),(0,0,0))
            self.surface.blit(status, [10,550])
        os = pygame.transform.rotozoom(self.icon,-self.asv_h,2)
        self.surface.blit(os,os.get_rect(center=(self.asv_x,self.asv_y)))
        self.display.blit(self.surface,[0,0])
        pygame.display.update()
        self.fps_clock.tick(RENDER_FPS)


if __name__ == '__main__':
    env = ASVLidarEnv(render_mode=None)#'human')
    env.reset()
    pygame.event.set_allowed((pygame.QUIT,pygame.KEYDOWN,pygame.KEYUP))
    action = CENTER
    total_reward = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                exit()
            elif event.type == pygame.KEYUP:
                action = CENTER
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    action = STBD
                elif event.key == pygame.K_LEFT:
                    action = PORT
        #print(rudder)
        obs,rew,term,_ = env.step(action)
        total_reward += rew
        if term:
            print(env.elapsed_time, total_reward)
            pygame.display.quit()
            pygame.quit()
            exit()
    
        

        

