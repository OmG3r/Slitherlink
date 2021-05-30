#https://antoinemeyer.frama.io/fltk/
import sys
import os
import re
height = 0
width = 0
indices = []
etat = {}
def lireJeu(filename = ""):
    global indices, height, width
    with open(filename) as file:
        lines = [line.rstrip('\n') for line in file]
    print(lines)
    
    if len(list(set([len(line) for line in lines]))) != 1:
        raise BaseException("lines length are not consistent")

    
    if False in [True if re.match(r'^([0123_])+$', line) else False  for line in lines]:
        raise BaseException("Invalid Characters detected")

    indices = [[int(letter) if letter.isdigit() else None for letter in list(line)] for line in lines]
    height = len(lines)
    width = len(lines[0])
    pass


def verifyTuplesOrder(segment):
    tup1 = segment[0]
    tup2 = segment[1]

    if tup1[0] > tup2[0]:
        return (tup2, tup1)

    if tup1[0] == tup2[0] and tup1[1] > tup2[1]:
        return (tup2, tup1)

    return segment

def est_trace(etat, segment):
    segment = verifyTuplesOrder(segment)
    if etat.get(segment, None) == 1:
        return True
    return False

def est_interdit(etat, segment):
    segment = verifyTuplesOrder(segment)
    if etat.get(segment, None) == -1:
        return True
    return False


def est_vierge(etat, segment):
    segment = verifyTuplesOrder(segment)
    if etat.get(segment, None) == None:
        return True
    return False

def tracer_segment(etat, segment):
    segment = verifyTuplesOrder(segment)
    if not est_vierge(etat, segment):
        raise BaseException("Segment not vierge")
    etat[segment] = 1

def tracer_segment(etat, segment):
    segment = verifyTuplesOrder(segment)
    if not est_vierge(etat, segment):
        raise BaseException("Segment not vierge")
    etat[segment] = -1

def effacer_segment(etat, segment):
    segment = verifyTuplesOrder(segment)
    etat.pop(segment, None)

def segments_traces(etat, sommet):
    segments = []
    for segment, status in etat.items():
        if status != 1:
            continue
        if sommet in list(segment): 
            segments.append(segment)

    return segments
    

def segments_interdits(etat, sommet):
    segments = []
    for segment, status in etat.items():
        if status != -1:
            continue
        if sommet in list(segment): 
            segments.append(segment)

    return segments
    

def  segments_vierges(etat, sommet):
    i, j = sommet


    candidates = [
        ((i, j), (i, j + 1)),
        ((i, j), (i + 1, j)),
        ((i,j), (i, j - 1)),
        ((i,j), (i - 1, j))
    ]
    
    segments = []
    for candidate in candidates:
        candidate = verifyTuplesOrder(candidate)
        if etat.get(candidates, False):
            segments.append(candidate)
    return segments
def statut_case(indices, etat, case):
    i, j = case
    indice = indices[i][j]
    if indice == None:
        return None
    pts = [
        (i,j),
        (i, j + 1),
        (i + 1, j + 1),
        (i + 1 , j)
    ]
    segments = [
        (pts[0], pts[1]),
        (pts[1], pts[2]),
        (pts[2], pts[3]),
        (pts[3], pts[0])
    ]
    segments = [verifyTuplesOrder(segment) for segment in segments]
    
    nber_trace = 0
    nber_veirge = 0
    nber_interdit = 0
    for segment in segments:
        nber_trace = nber_trace + int(est_trace(etat, segment))
        nber_veirge = nber_veirge + int(est_vierge(etat, segment))
        nber_interdit = nber_interdit + int(est_interdit(etat, segment))
    pass

    if nber_trace== indice:
        return 0

    if (nber_trace < indice) and (nber_trace + nber_interdit < 4) and (nber_veirge > 0):
        return 1

    if (nber_trace > indice) or (nber_veirge < indice - nber_trace):
        return -1

    
lireJeu("./grilles/grille1.txt")

