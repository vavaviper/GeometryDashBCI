import argparse
import time
import numpy as np
import collections
import pyautogui
import pydirectinput
import pandas as pd
import matplotlib.pyplot as plt

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions


def main ():

    params = BrainFlowInputParams ()
    params.board_id = 1
    board_id = 1
    params.serial_port = 'COM3'
    sampling_rate = BoardShim.get_sampling_rate (board_id)

    time_thres =  100
    max_val = -100000000000
    vals_mean = 0
    num_samples = 5000
    samples = 0

    BoardShim.enable_dev_board_logger ()

    board = BoardShim (board_id, params)
    board.prepare_session ()


    if board_id == brainflow.board_shim.BoardIds.GANGLION_BOARD.value:
        board.config_board ('x1060000X')

    board.start_stream (45000)


    print("starting calibration")
    time.sleep(5)
    data = board.get_board_data()

    print("start blinking")

    while(samples < num_samples):

        data = board.get_board_data() 
        if(len(data[1]) > 0):
            DataFilter.perform_rolling_filter (data[1], 2, AggOperations.MEAN.value)
            vals_mean += sum([data[1,i]/num_samples for i in range(len(data[1]))]) 
            samples += len(data[1])
            if(np.amax(data[1]) > max_val):
                max_val = np.amax(data[1])
 
    blink_thres = 0.5*((max_val - vals_mean)**2) 

    print("mean value")
    print(vals_mean)
    print("max value")
    print(max_val)
    print("threshold")
    print(blink_thres)


    print("CALIBRATION DONE START PLAYING")
    prev_time = int(round(time.time() * 1000))

    while True:

        data = board.get_board_data()

        if(len(data[1]) > 0):
            DataFilter.perform_rolling_filter (data[1], 2, AggOperations.MEAN.value) 
            if((int(round(time.time() * 1000)) - time_thres) > prev_time): 
                prev_time = int(round(time.time() * 1000))
                for element in data[1]:
                    if(((element - vals_mean)**2) >= blink_thres):
                        pydirectinput.press('space')
                        break                 

    board.stop_stream ()                   
    board.release_session ()


if __name__ == "__main__":
    main ()