import tkinter
import turtle
import codecs
import sys
import psutil
import pygame
import pynput
file = codecs.open(sys.argv[1],"r","utf-8")
c = file.read()
file.close()
exec(c)
