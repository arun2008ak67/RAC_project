import cv2
import numpy as np

# ==========================================
# OPENCV PROJECT - TASK MENU
# ==========================================

IMAGE_PATH = "test.jpeg"


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def load_image():
    image = cv2.imread(IMAGE_PATH)

    if image is None:
        print("Error: Image could not be loaded.")
        print("Keep test.jpeg in the same folder as this file.")
        return None

    return image


def open_camera():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        cap.release()
        return None

    return cap


def create_red_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red range 1
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])

    # Red range 2
    lower_red2 = np.array([165, 100, 100])
    upper_red2 = np.array([179, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = cv2.bitwise_or(mask1, mask2)

    return mask


def close_camera(cap):
    if cap is not None:
        cap.release()

    cv2.destroyAllWindows()


# ==========================================
# TASK 1 - OPENCV VERSION AND IMAGE
# ==========================================

def task1():
    print("OpenCV Version:", cv2.__version__)

    image = load_image()

    if image is None:
        return

    print("Image loaded successfully")
    print("Shape:", image.shape)

    cv2.imshow("My Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ==========================================
# TASK 3 - IMAGE DIMENSIONS AND PIXELS
# ==========================================

def task3():
    image = load_image()

    if image is None:
        return

    height, width, channels = image.shape

    print("Height:", height)
    print("Width:", width)
    print("Channels:", channels)

    if height > 100 and width > 100:
        pixel = image[100, 100]
        print("Pixel value:", pixel)
    else:
        print("Image is too small for pixel (100, 100).")

    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ==========================================
# TASK 4 - LIVE CAMERA
# ==========================================

def task4():
    cap = open_camera()

    if cap is None:
        return

    try:
        print("Press Q to quit.")

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Could not read camera.")
                break

            cv2.imshow("Live Camera", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        close_camera(cap)


# ==========================================
# TASK 4A - CAMERA TEST
# ==========================================

def task4a():
    cap = open_camera()

    if cap is None:
        return

    try:
        ret, frame = cap.read()

        print("Frame received:", ret)

        if ret:
            print("Frame shape:", frame.shape)
            cv2.imshow("Camera Test", frame)
            cv2.waitKey(0)
        else:
            print("Could not capture frame.")

    finally:
        close_camera(cap)


# ==========================================
# TASK 5 - GRAYSCALE
# ==========================================

def task5():
    image = load_image()

    if image is None:
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    print("Color shape:", image.shape)
    print("Gray shape:", gray.shape)

    cv2.imshow("Original Color", image)
    cv2.imshow("Grayscale", gray)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ==========================================
# TASK 6 - RESIZE
# ==========================================

def task6():
    image = load_image()

    if image is None:
        return

    small = cv2.resize(image, (200, 200))

    print("Original shape:", image.shape)
    print("Resized shape:", small.shape)

    cv2.imshow("Original", image)
    cv2.imshow("Resized", small)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ==========================================
# TASK 7 - CROP / ROI
# ==========================================

def task7():
    image = load_image()

    if image is None:
        return

    crop = image[50:500, 100:350]

    if crop.size == 0:
        print("Error: Crop region is empty.")
        return

    print("Original shape:", image.shape)
    print("Crop shape:", crop.shape)

    cv2.imshow("Original", image)
    cv2.imshow("Crop", crop)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ==========================================
# TASK 8 - DRAWING
# ==========================================

def task8():
    image = load_image()

    if image is None:
        return

    # Rectangle
    cv2.rectangle(
        image,
        (100, 50),
        (300, 300),
        (0, 255, 0),
        2
    )

    # Circle
    cv2.circle(
        image,
        (200, 200),
        50,
        (255, 0, 0),
        3
    )

    # Text
    cv2.putText(
        image,
        "RAC OpenCV",
        (50, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Drawing", image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ==========================================
# TASK 9 - RED COLOR MASK
# ==========================================

def task9():
    cap = open_camera()

    if cap is None:
        return

    try:
        print("Show a red object to the camera.")
        print("Press Q to quit.")

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Could not read camera.")
                break

            mask = create_red_mask(frame)

            cv2.imshow("Original", frame)
            cv2.imshow("Red Mask", mask)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        close_camera(cap)


# ==========================================
# TASK 9A - INSPECT HSV VALUES
# ==========================================

def task9a():
    cap = open_camera()

    if cap is None:
        return

    current_frame = [None]

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            frame = current_frame[0]

            if frame is None:
                return

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            print("Position:", x, y)
            print("BGR:", frame[y, x])
            print("HSV:", hsv[y, x])
            print("--------------------")

    try:
        cv2.namedWindow("Camera")
        cv2.setMouseCallback("Camera", mouse_callback)

        print("Click on the camera image to inspect HSV values.")
        print("Press Q to quit.")

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Could not read camera.")
                break

            frame = cv2.flip(frame, 1)
            current_frame[0] = frame.copy()

            cv2.imshow("Camera", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        close_camera(cap)


# ==========================================
# TASK 10 - CONTOURS
# ==========================================

def task10():
    cap = open_camera()

    if cap is None:
        return

    try:
        print("Show a red object to the camera.")
        print("Press Q to quit.")

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Could not read camera.")
                break

            mask = create_red_mask(frame)

            contours, _ = cv2.findContours(
                mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            cv2.putText(
                frame,
                f"Contours: {len(contours)}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.imshow("Contours", frame)
            cv2.imshow("Mask", mask)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        close_camera(cap)


# ==========================================
# TASK 11 - CONTOUR AREA
# ==========================================

def task11():
    cap = open_camera()

    if cap is None:
        return

    try:
        print("Show a red object to the camera.")
        print("Press Q to quit.")

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Could not read camera.")
                break

            mask = create_red_mask(frame)

            contours, _ = cv2.findContours(
                mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            for contour in contours:
                area = cv2.contourArea(contour)

                if area > 1000:
                    x, y, w, h = cv2.boundingRect(contour)

                    cv2.rectangle(
                        frame,
                        (x, y),
                        (x + w, y + h),
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        frame,
                        f"Area: {int(area)}",
                        (x, max(y - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2
                    )

            cv2.imshow("Contour Area", frame)
            cv2.imshow("Mask", mask)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        close_camera(cap)


# ==========================================
# TASK 12 - BOUNDING BOX
# ==========================================

def task12():
    cap = open_camera()

    if cap is None:
        return

    try:
        print("Show a red object to the camera.")
        print("Press Q to quit.")

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Could not read camera.")
                break

            mask = create_red_mask(frame)

            contours, _ = cv2.findContours(
                mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            if contours:
                largest = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest)

                if area > 1000:
                    x, y, w, h = cv2.boundingRect(largest)

                    cv2.rectangle(
                        frame,
                        (x, y),
                        (x + w, y + h),
                        (0, 255, 0),
                        2
                    )

                    print(
                        f"x: {x}, y: {y}, "
                        f"width: {w}, height: {h}"
                    )

            cv2.imshow("Bounding Box", frame)
            cv2.imshow("Red Mask", mask)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        close_camera(cap)


# ==========================================
# TASK 13 - RED OBJECT CENTER DETECTION
# ==========================================

def task13():
    cap = open_camera()

    if cap is None:
        return

    try:
        print("Show a red object to the camera.")
        print("Press Q to quit.")

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Could not read camera.")
                break

            frame = cv2.flip(frame, 1)
            mask = create_red_mask(frame)

            contours, _ = cv2.findContours(
                mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            if contours:
                largest = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest)

                if area > 1000:
                    x, y, w, h = cv2.boundingRect(largest)

                    cx = x + w // 2
                    cy = y + h // 2

                    cv2.rectangle(
                        frame,
                        (x, y),
                        (x + w, y + h),
                        (0, 255, 0),
                        2
                    )

                    cv2.circle(
                        frame,
                        (cx, cy),
                        5,
                        (0, 0, 255),
                        -1
                    )

                    cv2.putText(
                        frame,
                        f"Center: ({cx}, {cy})",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )

            cv2.imshow("Detection", frame)
            cv2.imshow("Red Mask", mask)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        close_camera(cap)


# ==========================================
# TASK 14 - LEFT / CENTER / RIGHT
# ==========================================

def task14():
    cap = open_camera()

    if cap is None:
        return

    try:
        print("Move a red object from left to right.")
        print("Press Q to quit.")

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Could not read camera.")
                break

            frame = cv2.flip(frame, 1)

            mask = create_red_mask(frame)

            contours, _ = cv2.findContours(
                mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            position = "NO OBJECT"

            if contours:
                largest = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest)

                if area > 1000:
                    x, y, w, h = cv2.boundingRect(largest)

                    cx = x + w // 2
                    cy = y + h // 2

                    width = frame.shape[1]

                    if cx < width / 3:
                        position = "LEFT"
                    elif cx < 2 * width / 3:
                        position = "CENTER"
                    else:
                        position = "RIGHT"

                    cv2.rectangle(
                        frame,
                        (x, y),
                        (x + w, y + h),
                        (0, 255, 0),
                        2
                    )

                    cv2.circle(
                        frame,
                        (cx, cy),
                        5,
                        (0, 0, 255),
                        -1
                    )

            cv2.putText(
                frame,
                position,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.imshow("Position Detection", frame)
            cv2.imshow("Red Mask", mask)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        close_camera(cap)


# ==========================================
# TASK 16 - TEST MEDIAPIPE
# ==========================================

def task16():
    try:
        import mediapipe as mp

        print("MediaPipe version:", mp.__version__)

    except ImportError:
        print("MediaPipe is not installed.")
        print("Run: python -m pip install mediapipe")


# ==========================================
# MAIN MENU
# ==========================================

def main():
    tasks = {
        "1": ("OpenCV Version and Image", task1),
        "3": ("Image Dimensions and Pixels", task3),
        "4": ("Live Camera", task4),
        "4a": ("Camera Test", task4a),
        "5": ("Grayscale Conversion", task5),
        "6": ("Resize Image", task6),
        "7": ("Crop / ROI", task7),
        "8": ("Drawing", task8),
        "9": ("Red Color Mask", task9),
        "9a": ("Inspect HSV Values", task9a),
        "10": ("Contours", task10),
        "11": ("Contour Area", task11),
        "12": ("Bounding Box", task12),
        "13": ("Red Object Center Detection", task13),
        "14": ("Left / Center / Right", task14),
        "16": ("Test MediaPipe", task16)
    }

    while True:
        print("\n" + "=" * 45)
        print("       OPENCV PROJECT - MAIN MENU")
        print("=" * 45)

        for key, (name, _) in tasks.items():
            print(f"{key:>3}. {name}")

        print("  0. Exit")
        print("=" * 45)

        choice = input("Enter task number: ").strip().lower()

        if choice == "0":
            print("OpenCV project closed.")
            break

        selected_task = tasks.get(choice)

        if selected_task is None:
            print("Invalid choice. Please try again.")
            continue

        task_name, task_function = selected_task

        print(f"\nRunning: {task_name}")

        try:
            task_function()

        except cv2.error as error:
            print("OpenCV error:", error)

        except Exception as error:
            print("Unexpected error:", error)

        input("\nPress Enter to return to the main menu.")


# ==========================================
# PROGRAM START
# ==========================================

if __name__ == "__main__":
    main()