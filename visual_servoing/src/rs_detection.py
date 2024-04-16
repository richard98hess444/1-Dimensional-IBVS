import cv2.cv2
import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge, CvBridgeError
import cv2
import cv2.aruco as aruco # type: ignore
import numpy as np
bridge = CvBridge()

depth_image_topic = '/camera/aligned_depth_to_color/image_raw'
rgb_image_topic = '/camera/color/image_raw' 

no_detect = -999

class ImageColorSubscriber():
    def __init__(self):  
        self.sub = rospy.Subscriber(rgb_image_topic, Image, self.imgColorCallback)
        self.img_color = None
        self.triggered = False

    def imgColorCallback(self, data):
        self.img_color = data
        self.triggered = True


def imageColorPub(data, coordinate):
    try:
        if coordinate[0] == no_detect:
            coordinate = [0, 0]
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
        cv_image = cv2.circle(cv_image, (int(coordinate[0]), int(coordinate[1])), radius=5, color=(0, 0, 255), thickness=-1)
        ros_img = bridge.cv2_to_imgmsg(cv_image, "bgr8")
        pub = rospy.Publisher("/realsense_img", Image, queue_size=20)
        pub.publish(ros_img)
    except CvBridgeError as e:
        print(e)
        return
    except ValueError as e:
        return

def arucoDetection(img_color):
    frame = bridge.imgmsg_to_cv2(img_color, "bgr8")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_50)
    parameters = aruco.DetectorParameters_create()

    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray,aruco_dict,parameters=parameters)

    if ids is not None:
        corners = np.mean(np.array(corners[0][0]), axis=0)
    else:
        corners = [no_detect, no_detect]
    
    feature = Point()
    feature.x = corners[0]
    feature.y = corners[1]
    feature.z = 0
    pub_feature = rospy.Publisher("/feature_coordinate", Point, queue_size=5)
    pub_feature.publish(feature)

    return corners


def main():
    color = ImageColorSubscriber()
    while (not color.triggered): pass

    while not rospy.is_shutdown():
        feature = arucoDetection(color.img_color)
        imageColorPub(color.img_color, feature)
    

if __name__ == '__main__':
    rospy.init_node("rs_detection")
    main()
