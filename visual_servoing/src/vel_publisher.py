import rospy
from std_msgs.msg import Float32

def talker(vel):
    if vel == 0:
        dt = 0
    elif vel > 0:
        dt = 19/(2*vel)
    elif vel < 0:
        dt = 19/(2*vel)
    pub = rospy.Publisher('cmd_linvel', Float32, queue_size=2)
    pub.publish(dt)

def velocity_filter(vel):
    if abs(vel) > 1.0:
        vel = 0
    return vel

if __name__ == '__main__':
    rospy.init_node('vel_publisher', anonymous=True)
    talker(0)
    try:
        while not rospy.is_shutdown():
            print('Enter -2 to 2: ')
            x = float(input())
            vel_filter = velocity_filter(x)
            talker(vel_filter)
    except rospy.ROSInterruptException:
        pass