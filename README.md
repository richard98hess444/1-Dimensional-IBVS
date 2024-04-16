# Launching the Package Steps by Steps

### 1. Realsense
```
roslaunch realsense2_camera rs_camera.launch align_depth:=true depth_width:=640 depth_height:=480 depth_fps:=30 color_width:=640 color_height:=480 color_fps:=30
```

### 2. Aruco Marker Detection
```
rosrun visual_servoing rs_detection.py
```

### 3. Arduino Serial
```
rosrun rosserial_python serial_node.py /dev/tty* # change with your device
```

### 4. IBVS Code
```
rosrun visual_servoing ibvs.py
```

### 5. Data Recorder (Optional)
Don't forget to change the path of the saved files.
```
rosrun visual_servoing data_record.py
```