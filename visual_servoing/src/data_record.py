import rospy
from geometry_msgs.msg import Point
from datetime import datetime
import numpy as np

filePath = '/home/richa/notebook/jupyterenv/notebook/visual_servoing/IBVS_data/'

class DataSubscriber():
    def __init__(self):  
        self.sub = rospy.Subscriber("/IBVS_data_recorder", Point, self.CoordinateCallback)
        self.vel = 0
        self.err = 0
        self.end = 0
        self.triggered = False

    def CoordinateCallback(self, data):
        self.vel = data.x
        self.err = data.y
        self.end = data.z
        self.triggered = True


def main():
    err_data = np.array([])
    velx_data = np.array([])
    data = DataSubscriber()

    while not data.triggered: pass
    while not rospy.is_shutdown():
        err_data = np.append(err_data, data.err)
        velx_data = np.append(velx_data, data.vel)
        rospy.sleep(0.05)

    now = datetime.now()
    current_time = now.strftime("%y%m%d_%H%M%S")
    np.save(filePath + 'err', err_data)
    np.save(filePath + 'velx', velx_data)
    print('saved')

if __name__ == '__main__':
    rospy.init_node("ibvs_record_node")
    main()
