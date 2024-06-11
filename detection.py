import torch
import cv2
import pathlib
import time

pathlib.PosixPath = pathlib.WindowsPath

model = torch.hub.load('ultralytics/yolov5', 'custom', path='weight\\bestm_2.pt')

cap = cv2.VideoCapture(0)

all_detected_classes = []
list=['0']
list2=[]
frequent_classes_str = ""
last_class = None  # Son tespit edilen sınıf
class_count = 0
start_time = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    df = results.pandas().xyxy[0]

    for _, row in df.iterrows():
        x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
        confidence = row['confidence']
        if confidence > 0.5:
            label = f"{row['name']} {row['confidence']:.2f}"
            all_detected_classes.append(row['name'])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


            if row['name'] == last_class:
                class_count += 1
            else:
                last_class = row['name']
                class_count = 1

            if class_count >= 10:
                list.append(row['name'])

                if list[-1] != list[-2]:
                    list2.append(list[-1])
                    frequent_classes_str = ''.join(list2)
                print(list2)
                class_count = 0


    if cv2.waitKey(1) & 0xFF == ord('k'):
        frequent_classes_str = ''.join(list2)
        print(f"Detected classes: {frequent_classes_str}")
        list.clear()
        list2.clear()
        list.append("0")
        all_detected_classes.clear()
        start_time = time.time()

    if cv2.waitKey(1) & 0xFF == ord(' '):
        list2.append(" ")
        print(list2)


    if cv2.waitKey(1) & 0xFF == ord('l'):
        frequent_classes_str = ""
        last_class = None
        class_count = 0
        start_time = None

    #cv2.putText(frame, frequent_classes_str, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if start_time and (time.time() - start_time) < 10:
        cv2.putText(frame, frequent_classes_str, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    elif start_time and (time.time() - start_time) >= 10:
        frequent_classes_str = ""
        start_time = None

    cv2.imshow('YOLOv5 Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
