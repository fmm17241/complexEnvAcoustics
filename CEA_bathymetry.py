# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 19:28:14 2024

Defining the bathymetry for our research array. Can easily change for other experiments.

Flat, which is a straight shot between instruments.
Linear, a linear slope between instruments.
Real, a realistic bathymetry between instruments.


FS17
T Depth: 17.8 m
W Depth: 19.4 m

STSNew1
T Depth: 13.7 m
W Depth: 15.8 m

SURTASSTN20
T Depth: 16.8 m
W Depth: 20.4 m

@author: fmm17241
"""

def simple2k(depth=18):
    return [
        [0, depth],    
        [2100, depth]
        ]

def simple1800(depth=20):
    return [
        [0, depth],    
        [1820, depth]
        ]

#FS17 to STSNew1, 668 meters away
def FS17toSTSNew1Flat(depth=19.4):
    return [
        [0, depth],    
        [200, depth],   
        [300, depth],  
        [350, depth],  
        [600, depth],  
        [670, depth]
    ]

def STSNew1toFS17Flat(depth=19.4):
    return [
        [0, depth],    
        [200, depth],   
        [300, depth],  
        [350, depth],  
        [600, depth],  
        [670, depth]
    ]


def FS17toSTSNew1Real(depth=19.4): # Attempting to connect FS17 and STSNew1
    return [ 
        [0, depth],
        [10, depth-1],
        [20, depth],
        [80, depth-2],
        [100, depth-2],
        [120, depth-2.5],
        [150, depth-3],
        [450, depth-3],
        [470, depth-4.6],
        [600, depth-4.2],
        [670, depth-4.2]
        ]

def STSNew1toFS17Real(depth=19.4): # Attempting to connect FS17 and STSNew1
    return [ 
        [0, depth-4.2],        
        [100, depth-4.2],
        [200, depth-4.6],
        [220, depth-3],
        [550, depth-3],
        [580, depth-2.5],
        [600, depth-2],
        [620, depth-2],
        [660, depth],
        [670, depth-1],
        ]

def FS17toSTSNew1Linear(depth=19.4): # 
    return [ 
        [0, depth],
        [670, depth-4.2]
        ]


def STSNew1toFS17Linear(depth=19.4): # 
    return [ 
        [0, depth-4.2],
        [100, depth-3.2],
        [200, depth-2.4],
        [300, depth-2],
        [400, depth-1.6],
        [500, depth-1.2],
        [600, depth-0.6],
        [670, depth]
        ]

##
# FS17 to SURT20, 1150 meters
def FS17toSURT20Flat(depth=20.4):
    return [
        [0, depth],    
        [200, depth],  
        [300, depth],  
        [350, depth],   
        [600, depth],  
        [800, depth],
        [900, depth],
        [1000, depth],
        [1100, depth],
        [1160, depth]
    ]


def SURT20toFS17Flat(depth=20.4):
    return [
        [0, depth],    
        [200, depth],  
        [300, depth],  
        [350, depth],  
        [600, depth],  
        [800, depth],
        [900, depth],
        [1000, depth],
        [1100, depth],
        [1160, depth]
    ]

#SURT20 to FS17
def FS17toSURT20Linear(depth=20.4):
    return [
        [0, depth-1],    
        [1160, depth]
    ]

def SURT20toFS17Linear(depth=20.4):
    return [
        [0, depth],    
        [200, depth],  
        [300, depth-0.1],  
        [400, depth-0.2],  
        [500, depth-0.3],  
        [550, depth-0.4],  
        [600, depth-0.5],  
        [800, depth-0.6],
        [900, depth-0.7],
        [1000, depth-0.8],
        [1100, depth-0.9],
        [1160, depth-1]
    ]

def FS17toSURT20Real(depth=20.4):
    return [
        [0, depth-1.0],
        [10, depth-1.0],
        [20, depth-1.0],
        [80, depth-1.0],
        [100, depth-1.5],
        [300, depth-2.5],
        [500, depth-3.5],
        [600, depth-5.0],
        [700, depth-3.5],  
        [800, depth-2.0],  
        [900, depth-0.6],  
        [1000, depth-0.6],
        [1050, depth-0.5],
        [1100, depth-2.5],
        [1150, depth],
        [1160, depth]
    ]

def SURT20toFS17Real(depth=20.4):
    return [
        [0, depth],
        [50, depth],
        [100, depth-2.5],
        [150, depth-0.5],
        [200, depth-0.6],
        [300, depth-0.6],
        [400, depth-2.0],
        [500, depth-3.5],
        [600, depth-5.0],  
        [700, depth-3.5],  
        [900, depth-2.5],  
        [1100, depth-1.5],
        [1120, depth-1.0],
        [1160, depth-1.0]
    ]

#SURT20 to STSNew1, 530 meters
#20.4 to 15.8
def SURT20toSTSNew1Flat(depth=20.4):
    return [
        [0, depth],    
        [200, depth],  
        [300, depth],  
        [350, depth],   
        [400, depth], 
        [450, depth],
        [500, depth],
        [550, depth]
    ]

#15.8 to 20.4
def STSNew1toSURT20Flat(depth=20.4):
    return [
        [0, depth],    
        [200, depth],  
        [300, depth],  
        [350, depth],   
        [400, depth],  
        [450, depth],
        [500, depth],
        [550, depth]
    ]

#15.8 to 20.4
def STSNew1toSURT20Linear(depth=20.4):
    return [
        [0, depth-4.6],    
        [550, depth]
    ]

def SURT20toSTSNew1Linear(depth=20.4):
    return [
        [0, depth],   
        [550, depth-4.6]
    ]

def SURT20toSTSNew1Real(depth=20.4):
    return [
        [0, depth],   
        [100, depth-0.5], 
        [120, depth-0.5], 
        [150, depth-3.0], 
        [250, depth-4.2], 
        [300, depth-4.2], 
        [350, depth-3.2],   
        [400, depth-0.5], 
        [450, depth-0.6],
        [500, depth-3.0],
        [550, depth-4.6]
    ]

def STSNew1toSURT20Real(depth=20.4):
    return [
        [0, depth-4.6],
        [50, depth-3.0],
        [100, depth-0.6], 
        [200, depth-3.4], 
        [250, depth-3.8], 
        [300, depth-4.2], 
        [350, depth-4.2],   
        [400, depth-3.0], 
        [430, depth-0.5],
        [450, depth-0.5],
        [550, depth]
    ]
