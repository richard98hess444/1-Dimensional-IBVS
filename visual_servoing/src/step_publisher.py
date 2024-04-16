import rospy
from std_msgs.msg import Float32

def talker(stp):
    pub = rospy.Publisher('cmd_step', Float32, queue_size=2)
    pub.publish(stp)

if __name__ == '__main__':
    rospy.init_node('step_publisher', anonymous=True)
    talker(0)
    try:
        while not rospy.is_shutdown():
            print('Enter -10000 to 10000: ')
            x = float(input())
            talker(x)
    except rospy.ROSInterruptException:
        pass