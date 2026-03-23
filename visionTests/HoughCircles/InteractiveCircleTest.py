import numpy as np
from BatteryLab.helper.Logger import Logger
from BatteryLab.robots.AutoCorrection import AutoCorrection
from BatteryLab.robots.Constants import AutoCorrectionConfig
import cv2
import sys
import os


def clear_terminal():
    """Clear the terminal screen in a cross-platform way."""
    os.system("cls" if os.name == "nt" else "clear")


def show_splash():
    """Clear the terminal and print a simple ASCII splash screen."""
    clear_terminal()
    splash = r"""     
        ____   @@@@@@@@@@@@               
       |====| @@.        .@@       
     :@@@@@@@@@.          .@@@@@@@@@:     
     @@.          .%@@%.          .@@     
     @@.       .@@@@==@@@@.       .@@     
     @@.      .@@.      .@@.      .@@     
     @@.      @@.        .@@      .@@     
     @@.     .@@.        .@@      .@@     
     @@.      %@@        @@%      .@@     
     @@.       *@@=    =@@*       .@@     
     @@.         .@@@@@@.         .@@     
     @@.                          .@@     
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 

Interactive Circle Detection Test
----------------------------------------------------
- Use trackbars to tune HoughCircles parameters.
- Press 'p' to print current parameters.
- Press 'i' to invert / restore image.
- Press 'q' or ESC to quit current image.
"""
    print(splash)


def get_screen_size() -> tuple[int, int]:
    """Best-effort way to get primary screen size using OpenCV."""
    tmp_name = "__tmp_fullscreen__"
    cv2.namedWindow(tmp_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(tmp_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    x, y, w, h = cv2.getWindowImageRect(tmp_name)
    cv2.destroyWindow(tmp_name)
    # Fallback to a sane default if detection fails
    if w <= 0 or h <= 0:
        return 1920, 1080
    return w, h


# Set up component configs
configs = AutoCorrectionConfig()

# Set up logger and AutoCorrection module
log_path = "/home/yuanjian/Research/BatteryLab/logs/"
logger = Logger("circle_detect_test", log_path, "circle_detect_test.log")
correcter = AutoCorrection(logger, silent=True)

# Define image path
# img_folder_path = "/home/yuanjian/Research/BatteryLab/images/"
img_folder_path = "./"

# --- helpers for directory / file handling ---

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}


def is_image_file(path: str) -> bool:
    _, ext = os.path.splitext(path.lower())
    return ext in IMAGE_EXTS


def list_images_in_dir(dir_path: str):
    files = []
    for name in sorted(os.listdir(dir_path)):
        full = os.path.join(dir_path, name)
        if os.path.isfile(full) and is_image_file(full):
            files.append(full)
    return files


# --- core interactive logic for a single image ---


def run_interactive_on_image(image_path: str):
    print(f"\n=== Processing image: {image_path} ===")
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        print(f"Failed to load image: {image_path}")
        return

    img_width = min(img.shape[:2])
    print(f"img_width={img_width}")

    object_config = {
        "minDist": img_width // 3,  # We only want one circle, so set this large
        "param1": 250,  # Too high will miss edges, too low -> noisy edges
        "param2": 30,  # Higher is stricter (fewer circles)
        "minR": 60,
        "maxR": 95,
    }

    img_name = os.path.basename(image_path)
    if "suction" in img_name:
        img = cv2.bitwise_not(img)  # invert image to more easily detect suction cup
        object_config["param2"] = 40
        object_config["minR"] = 40
        object_config["maxR"] = 80

    # Make a working copy so we don't destroy original defaults
    interactive_config = object_config.copy()

    # keep original image and a possibly inverted version
    original_img = img.copy()
    display_img = img.copy()
    inverted = False

    # --- callback closures using the local interactive_config/img ---

    def update(_=None):
        """Run detection and redraw using current interactive parameters."""
        # always detect on the currently displayed image
        found_circles = correcter.detect_object_center(display_img, interactive_config)
        print(f"found_circles: {found_circles}")

        # draw_detection crashes if found_circles is empty, so guard it
        if found_circles:
            newimage = correcter.draw_detection(display_img.copy(), found_circles)
        else:
            newimage = display_img.copy()

        cv2.imshow("Identified Circles", newimage)

    def set_minDist(v):
        interactive_config["minDist"] = max(1, v)  # minDist must be >= 1
        update()

    def set_param1(v):
        interactive_config["param1"] = max(1, v)  # param1 must be >= 1
        update()

    def set_param2(v):
        interactive_config["param2"] = max(1, v)  # param2 must be >= 1
        update()

    def set_minR(v):
        interactive_config["minR"] = max(1, v)  # min radius must be >= 1
        # Ensure maxR >= minR to avoid invalid range
        if interactive_config["maxR"] < interactive_config["minR"]:
            interactive_config["maxR"] = interactive_config["minR"]
            cv2.setTrackbarPos("maxR", "Identified Circles", interactive_config["maxR"])
        update()

    def set_maxR(v):
        interactive_config["maxR"] = max(interactive_config["minR"], v)  # maxR >= minR
        update()

    # Create / reset window and trackbars
    cv2.namedWindow("Identified Circles", cv2.WINDOW_NORMAL)

    # Dynamically size to 1/8th of the screen area (1/4 width, 1/2 height)
    screen_w, screen_h = get_screen_size()
    win_w = max(640, screen_w // 3)  # keep a minimum sensible size
    win_h = max(480, screen_h // 2)
    cv2.resizeWindow("Identified Circles", win_w, win_h)

    cv2.createTrackbar(
        "minDist",
        "Identified Circles",
        interactive_config["minDist"],
        img_width,
        set_minDist,
    )
    cv2.createTrackbar(
        "param1", "Identified Circles", interactive_config["param1"], 500, set_param1
    )
    cv2.createTrackbar(
        "param2", "Identified Circles", interactive_config["param2"], 200, set_param2
    )
    cv2.createTrackbar(
        "minR", "Identified Circles", interactive_config["minR"], img_width, set_minR
    )
    cv2.createTrackbar(
        "maxR", "Identified Circles", interactive_config["maxR"], img_width, set_maxR
    )

    # Run once at startup using original defaults
    update()

    # Handle exit gracefully
    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == ord("q") or k == 27:  # q or ESC
            break
        if k == ord("p"):
            print("\nCurrent object_config:")
            print("{")
            for k2, v2 in interactive_config.items():
                print(f"    '{k2}': {v2},")
            print("}")
        if k == ord("i"):
            # toggle inversion of the base image
            inverted = not inverted
            if inverted:
                display_img[:] = cv2.bitwise_not(original_img)
                print("Image inverted.")
            else:
                display_img[:] = original_img
                print("Image restored to original.")
            update()
        if cv2.getWindowProperty("Identified Circles", cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()  # Redundant. Shuts all cv2 windows.
    print("Image test complete")


# --- main entrypoint: support file or directory ---


def main():
    show_splash()
    if len(sys.argv) > 1:
        arg_path = sys.argv[1]
    else:
        print("No image or directory provided by user. Exiting.")
        return

    # If given a directory, process all images in it
    if os.path.isdir(arg_path):
        dir_path = arg_path
        images = list_images_in_dir(dir_path)
        if not images:
            print(f"No image files found in directory: {dir_path}")
            return

        print(f"Found {len(images)} image(s) in '{dir_path}':")
        for i, p in enumerate(images, 1):
            print(f"  [{i}] {p}")

        resp = (
            input("Run interactive test on all of these images? [Y/n]: ")
            .strip()
            .lower()
        )
        if resp not in ("", "y", "yes"):
            print("Aborted by user.")
            return

        for img_path in images:
            run_interactive_on_image(img_path)

        print("Directory test complete")
        return

    # Otherwise treat as file path or name in img_folder_path
    if os.path.isfile(arg_path):
        image_path = arg_path
    else:
        # fall back to original behavior: treat as name in img_folder_path
        image_path = os.path.join(img_folder_path, arg_path)

    run_interactive_on_image(image_path)
    print("Test complete")


if __name__ == "__main__":
    main()
