import pygame
import math

def detect_collision(obj1, obj2):
    """General collision-detection that can take any 2 game-objects"""
    if obj1.type == 1: #If the object is an area object
        for circle in obj1.circles:
            minimal_distance = circle.radius + obj2.radius
            current_distance = math.sqrt((math.fabs(float(circle.x - obj2.x)))**2 + (math.fabs(float(circle.y - obj2.y)))**2 )

            if current_distance <= minimal_distance:
                break

    elif obj2.type == 1: #If the object is an area object
        for circle in obj2.circles:
            minimal_distance = circle.radius + obj1.radius
            current_distance = math.sqrt((math.fabs(float(circle.x - obj1.x)))**2 + (math.fabs(float(circle.y - obj1.y)))**2 )

            if current_distance <= minimal_distance:
                break

    else:
        minimal_distance = obj1.radius + obj2.radius
        current_distance = math.sqrt((math.fabs(float(obj1.x - obj2.x)))**2 + (math.fabs(float(obj1.y - obj2.y)))**2 )

    if current_distance <= minimal_distance:
        return True
    else:
        return False
