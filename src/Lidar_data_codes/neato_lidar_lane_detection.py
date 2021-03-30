import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import pandas as pd
from scipy.optimize import curve_fit
#import seaborn as sns
#import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np
import math
import time
import serial

range_df = pd.DataFrame()
intensity_df = pd.DataFrame()
intensity_thresh = 1300
msgs_num_pline = 15 # pipeline of number of messages
column_ind = [*range(335,360,1)]+[*range(0,26,1)]
# Below deg value corresponds to 0 deg of the vehicle which means the vehicle centre.
# 26 because we have selected only 51 angular data points from 0 to 51 hence centre would be 26.
vehicle_centre = 26 

# setting up the serial communication channel for arduino
ser = serial.Serial('/dev/ttyUSB0', 9600)

def lane_detection(msg):
    
    global range_df, intensity_df, intensity_thresh, msgs_num_pline, column_ind
    
    '''
    ind_max = msg.intensities.index(max(msg.intensities))
    ind_min = msg.intensities.index(min(msg.intensities))
    #print(type(msg.intensities[335]))
    #print('maximum distance ' +str(msg.ranges[ind])+ ' at ' +str(ind) +'\n'+'intensity ' +str(msg.intensities[ind])+ ' at ' +str(ind))
    #print('Maximum intensity '+str(max(msg.intensities))+' at '+str(ind_max))
    #print('Minimum intensity '+str(min(msg.intensities))+' at '+str(ind_min))
    #print(type([msg.ranges[335:]+msg.ranges[:26]]))
    '''
    
    # appending the sliced zone data in which the retro reflective tape points are recorded
    range_zone = pd.DataFrame([msg.ranges[335:]+msg.ranges[:26]])
    int_zone = pd.DataFrame([msg.intensities[335:]+msg.intensities[:26]])
    
    #range_df = range_df.append(range_zone[int_zone > 1000])
    #intensity_df = intensity_df.append(int_zone[int_zone > 1000])
    range_df = range_df.append(range_zone)
    intensity_df = intensity_df.append(int_zone)
    
    if intensity_df.shape[0] == msgs_num_pline:
        
        start_t = time.time()
        
        arr_size = range_df.shape[0]
        range_df = range_df.set_index([pd.Index([*range(1,arr_size+1,1)])])
        intensity_df = intensity_df.set_index([pd.Index([*range(1,arr_size+1,1)])])
        
        '''
        plt.figure(figsize=(15,10))

        for i in range(0,arr_size,1):
            sns.scatterplot(range_df.iloc[i], range_df.columns, hue=intensity_df.iloc[i], 
                            palette='jet', legend=False)

        plt.axhline(y=26, color='r', linestyle='--')
        '''
        
        lane_range = range_df[intensity_df > intensity_thresh]
        lane_int = intensity_df[intensity_df > intensity_thresh]
        
        '''
        plt.figure(figsize=(15,10))

        for i in range(0,arr_size,1):
            sns.scatterplot(lane_range.iloc[i], lane_range.columns, hue=lane_int.iloc[i], 
                            palette='jet', legend=False, size=lane_int.iloc[i])       
        '''
            
            
        def lanecurve_fit(start, end):
    
            x_range = []
            y_angle = []

            for idx in range(start,end,1):
                for id_col in range(0, lane_range.shape[0],1):
                    if not np.isnan(lane_range.iloc[id_col, idx]):
                        x_range.append(lane_range.iloc[id_col, idx])
                        y_angle.append(idx)

            # define the true objective function
            def objective(x, a, b, c, d):
                return a * x + b * x**2 + c * x**2 + d
            
            if len(x_range) >= 10:
                # curve fit
                popt, _ = curve_fit(objective, x_range, y_angle)

                a, b, c, d = popt

                x_line = np.arange(min(x_range), max(x_range)+0.01, 0.01)
                y_line = objective(x_line, a, b, c, d)
            
            else:
                x_line = []
                y_line = []
                
            return x_line, y_line
        
        
        right_lanex, right_laney = lanecurve_fit(0,(lane_range.shape[1]-25))
        left_lanex, left_laney = lanecurve_fit(25,lane_range.shape[1])
        midlane_x = [np.mean([right_lanex[i], left_lanex[i]]) 
                     for i in range(min([len(right_lanex), len(left_lanex)]))]
        midlane_y = [np.mean([right_laney[i], left_laney[i]]) 
                     for i in range(min([len(right_laney), len(left_laney)]))]
        
        if len(midlane_x) > 0 and len(midlane_y) > 0:
            
            centre_error = round((vehicle_centre - midlane_y[0]),2)
            if centre_error < 0:
                print('The centre error = '+str(centre_error)+' to the LEFT')
            else:
                print('The centre error = '+str(centre_error)+' to the RIGHT')
                
            error_encode = b'%f' %centre_error
            
            ser.write(error_encode)
            '''
            plt.figure(figsize=(14,7))
            for i in range(0, arr_size,1):
                sns.scatterplot(lane_range.iloc[i], lane_range.columns, hue=lane_int.iloc[i], 
                                palette='jet', legend=False, 
                                size=lane_int.iloc[i])

            plt.plot(right_lanex, right_laney, '--', color='red')
            plt.plot(left_lanex, left_laney, '--', color='red')
            plt.plot(midlane_x, midlane_y, '--', color='blue')
            
            plt.pause(1)
            '''
        
        range_df = pd.DataFrame()
        intensity_df = pd.DataFrame()
        
        end_t = time.time()
        total_time = end_t - start_t
        
        print('total time elapsed = '+str(total_time)+' seconds')
    


rospy.init_node('obstacle_avoidance')
sub = rospy.Subscriber('/scan', LaserScan, lane_detection)
#pub = rospy.Publisher('/cmd_vel', Twist)
#move=Twist()
rospy.spin()
