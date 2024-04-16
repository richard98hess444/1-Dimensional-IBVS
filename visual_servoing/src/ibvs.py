import rospy
from geometry_msgs.msg import Point
from std_msgs.msg import Float32
import numpy as np

z_est = 0.2
no_detect = -999
camera_pinhole = np.array([[380.0203857421875,   0.              , 321.3174133300781],
                           [  0.             , 379.79266357421875, 249.7012481689453],
                           [  0.             ,   0.              ,   1.             ]])
Mc = camera_pinhole[:-1, :-1]*(1/z_est)
ref = np.array([320, 240])
Kp = 5




class CoordinateSubscriber():
    def __init__(self):  
        self.sub = rospy.Subscriber("/feature_coordinate", Point, self.CoordinateCallback)
        self.u = no_detect
        self.v = no_detect
        self.triggered = False

    def CoordinateCallback(self, data):
        self.u = data.x
        self.v = data.y
        self.triggered = True

def ArduinoPub(vel):
    if vel == 0:
        dt = 0
    elif vel > 0:
        dt = 19/(2*vel)
    elif vel < 0:
        dt = 19/(2*vel)
    pub_vel = rospy.Publisher('cmd_linvel', Float32, queue_size=2)
    pub_vel.publish(dt)

def dataPub(vel, err, end):
    data = Point()
    data.x = vel
    data.y = err
    data.z = end
    pub_data = rospy.Publisher('IBVS_data_recorder', Point, queue_size=5)
    pub_data.publish(data)

def velocity_filter(vel):
    if abs(vel) > 1.0:
        vel = 0
    return vel

def main():
    cord = CoordinateSubscriber()
    while not cord.triggered: pass

    while not rospy.is_shutdown():
        if [cord.u, cord.v] != [no_detect, no_detect]:
            feat = np.array([cord.u, cord.v])
            err = err = np.array([[0,0]]).T if abs(feat[0] - ref[0]) < 5 else (feat - ref).reshape(2,-1)
            vel = -Kp * np.linalg.inv(Mc) @ err

            vel_x = vel[0][0]
            vel_y = vel[1][0]

            vel_x = velocity_filter(vel_x)
            ArduinoPub(vel_x)
            dataPub(vel_x, err[0][0], 1)
            
            
if __name__ == '__main__':
    rospy.init_node("ibvs_node")
    main()


# err = (feat - ref).reshape(2,-1)
# if abs(feat[0] - ref[0]) < 5: 
#     err = np.array([[0,0]]).T

# print('error', round(err[0][0], 4))
# print('velocity', round(vel_x,4))
# rospy.sleep(0.1)