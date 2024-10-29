# Autonomous Surface Vessel (ASV) with LIDAR, for Gymnasium
This repository contains an implementation of the Gymnasium environment based on a simple ASV with a LIDAR sensor. It was greatly inspired by [flappy-bird-gymnasium](https://github.com/markub3327/flappy-bird-gymnasium/blob/main/README.md?plain=1).

## Observation space
A set of observations are made available:

* LIDAR scan - An array of range measurements from the ASV to any obstacles in range
* ASV Positoin - X,Y position of the ASV
* Heading - Heading/Yaw of the ASV
* Yaw Rate - rate of change of the heading
* Target - Horizontal offset of the ASV from the desired path

## Action space
* 0 - Rudder to Port (left)
* 1 - Rudder to center
* 2 - Rudder to Starboard (right)

## Rewards
* -1.0 - every step
* 0.0 - if ASV is near/on the path
* -10.0 - if ASV is not moving foward
* -20.0 - if ASV collides with Obstacle (not yet implemented)
