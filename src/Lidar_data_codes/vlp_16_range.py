import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import pandas as pd

lanezone_df = pd.DataFrame([])

def callback(msg):
	print('=======================================')
       # print('s1 [360]')
       # print msg.ranges[360]
       # print('s2 [0]')
       # print msg.ranges[0]
       # print('s3 [90]')
       # print msg.ranges[90]
	ind_max = msg.intensities.index(max(msg.intensities))
	ind_min = msg.intensities.index(min(msg.intensities))
	ind = 12
	print('maximum distance ' +str(msg.ranges[ind])+ ' at ' +str(ind) +'\n'
		+'intensity ' +str(msg.intensities[ind])+ ' at ' +str(ind))
	print('Maximum intensity '+str(max(msg.intensities))+' at '+str(ind_max))
	print('Minimum intensity '+str(min(msg.intensities))+' at '+str(ind_min))


       # if msg.ranges[360]>1.75:
        #        move.linear.x = 1
         #       move.angular.z = 0.0
       # else:
        #        move.linear.x = 0
         #       move.angular.z = 0.0

       # pub.publish(move)

rospy.init_node('obstacle_avoidance')
sub = rospy.Subscriber('/scan', LaserScan, callback)
#pub = rospy.Publisher('/cmd_vel', Twist)
#move=Twist()
rospy.spin()
