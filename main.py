# Tetris
import sys
import pygame
from ConfigurePage import ConfigurePage
from StartupPage import StartupPage
from GamePage import PlayGame

def main():
    startupPage = StartupPage()
    startupPage.RunStartup()

if __name__ == "__main__":
    main()
