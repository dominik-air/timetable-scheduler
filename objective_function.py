#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

def gaps_penalty(w1: float, o: np.ndarray) -> float:
    return np.squezze(np.sum(w1 * o))

def unbalanced_penalty(w2: float, H: int, h: np.ndarray) -> float:
    return np.squezze(np.sum(w2 * np.abs(H / 5 - h)))
