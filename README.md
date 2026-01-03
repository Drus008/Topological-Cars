# Topological-Cars
Race on surfaces that defy standard geometry.

Topological-Cars is a time-attack racing game where the track isn't just a flat loop, it's a mathematical object. Race against ghost data from previous players on surfaces like the Klein Bottle or Projective Plane.

## Gameplay
The premise is simple: Complete 3 laps and beat your opponent's time. However, the track topology may contradict your usual intuition of space and directions.


### Race Tracks
There are a variety of tracks to race on. Each one is determined by the following two characteristics:


#### Maps
The map determines the shape of the track. There are 2 options to select from:

- Pseudo-Circle: A simple map to help you grasp the basics of topological racing. It is homeomorphic to a circle, but navigation feels distinct.

- Z-homology: A more advanced map with various paths where you would have to make decision based on which one seems faster.


#### Topological spaces
The space influences the geometry of the track, making it tweak and bend in unexpected ways
There are 3 different topological surfaces to select from:

- Torus: A nice and intuitive surface, easily visualizable on our three-dimensional space. But maybe not so inutitive to race on.

- Klein bottle: The famous closed surface, first noticed by Felix Klein, that doesn't have an interior nor an exterior.

- Projective plane: Used more often in day to day life than the previous ones, but the one with the most mysterious geometry by far: where parallel lines cross and loops suddenly collapse when traversed twice.

### Opponents
Choose between players that have previously raced on each track and compete against their ghost to try to beat its time.

If you write your name, your run will be saved so the next player can challenge you.


### How to play
To open the menu you have to execute the `main.py` file.

#### Main Menu
- Choose map, space, rival by clicking on its corresponding section.
- Choose a name (max 15 characters) by typing it on its corresponding section.
- Press the button start to begin the race with the selected configuration.

#### Controls
| Key | Action |
| :---: | :--- |
| `W` | Accelerate |
| `S` | Reverse |
| `A` | Turn Left |
| `D` | Turn Right |
| `ESC` | Return to the Title Menu |


#### Saves

When you complete 3 laps your record will be saved if improved the previous record asigned to the specified name.

## Motivation
This project was developed as a university project from a course of Advanced Programming (Programació avançada from the fourth year of the Mathematics degree of Universitat Autónoma de Barcelona) taught by Vicens Soler Ruíz.

The project required to develop a driving game focusing on OOP in the base code and developed using tkinter, without other libraries (like pygame, or CustomTkinter).

I would love to add some aesthetic components to improve the game feel, but `tkinter` has severe limitation in terms of drawing multiple objects don't allow me. Maybe a port to Godot will be considered.

## Dependencies
- `numpy`
- `colormath`
- `PIL`

## Credits

Author: Drus Sentís Cahué (Drus008)