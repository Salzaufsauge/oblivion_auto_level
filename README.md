# oblivion_auto_level

A Python script to automate some stuff in Oblivion if you can't be bothered to press the buttons yourself

Originally used pyautogui/pydirectinput but sadly they didn't work as the input didn't get recognized by the game, so I
had to resort to ctypes.

This script is very basic and doesn't do much besides spamming some keys.

I might add some more features for leveling later.

## Features

- auto cast spells
- auto jump
- auto use quick menu with delay (can be used for potions)
- auto level sneak

## Installation

Clone with git and then run main.py like any other python script

## Usage/Examples

To use this script, follow the instructions and choose combo keys that are not already assigned

The hotkeys start with alt or right ctrl as left ctrl is default mapped to sneaking

## Acknowledgements

- [Source for the ctypes code](https://stackoverflow.com/questions/54624221/simulate-physical-keypress-in-python-without-raising-lowlevelkeyhookinjected-0/54638435#54638435)