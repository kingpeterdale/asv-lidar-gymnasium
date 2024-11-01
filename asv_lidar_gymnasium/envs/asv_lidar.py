import pygame
import numpy as np

LIDAR_RANGE = 150
LIDAR_SWATH = 90
LIDAR_BEAMS = 21

class Lidar:
    """ Basic LIDAR simulator.

        Utilises pygame rects to determine array of ranges
    """
    def __init__(self):
        self._pos_x = 0
        self._pos_y = 0
        self._hdg = 0
        self._angles = None
        self._ranges = None
        self.reset()


    def reset(self):
        """ Reset LIDAR 
        """
        self._pos_x = 0
        self._pos_y = 0
        self._hdg = 0
        self._angles = np.linspace(-LIDAR_SWATH/2,LIDAR_SWATH/2,LIDAR_BEAMS,dtype=np.int16)
        self._ranges = np.ones_like(self._angles) * LIDAR_RANGE


    @property
    def angles(self):
        """ array of sensor angles """
        return self._angles.copy()
    
    @property
    def ranges(self):
        """ array of ranges from most recent scan """
        return self._ranges.copy()
    
    
    def scan(self, pos, hdg, obstacles=None) -> np.ndarray:
        """ Perform a LIDAR scan

            Args:
                pos (tuple): x,y position of sensor
                hdg (float): orientation of sensor in degrees
                obstacles (list): list of obstacle rects
            Returns:
                array of ranges from sensor to obstacles. 
                If no obstacle reads LIDAR_RANGE
        """
        self._pos_x = pos[0]
        self._pos_y = pos[1]
        self._hdg = hdg
        # TODO: update self.ranges
        return self._ranges.copy()
        
        
    def render(self, surface:pygame.Surface):
        """ Render the LIDAR as a series of lines

            Args:
                surface (pygame.Surface): surface to render to
        """
        for idx,a in enumerate(self._angles):
            r = np.radians(self._hdg + a)
            x = self._pos_x + self._ranges[idx] * np.sin(r)
            y = self._pos_y - self._ranges[idx] * np.cos(r)
            pygame.draw.aaline(surface,(90,90,200),(self._pos_x,self._pos_y),(x,y))