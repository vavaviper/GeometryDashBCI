import argparse
import time
import numpy as np
import collections
import pyautogui
import pandas as pd
import matplotlib.pyplot as plt

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions

def main ():
    params = BrainFlowInputParams()
    params.board_id = 1
    board_id = 1
    params.serial_port = 'COM3'
    sampling_rate = BoardShim.get_sampling_rate (board_id)

    time_thres =  100
    max_val = -100000000000
    vals_mean = 0
    num_samples = 5000
    samples = 0

    BoardShim.enable_board_logger()

    board = BoardShim (board_id, params)
    board.prepare_session ()

    board.start_stream (45000, 'COM3')

    print("Starting calibration")
    time.sleep(5) # wait for data to stabilize
    data = board.get_board_data() # clear buffer
    
    print("blink a few times")