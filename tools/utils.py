import os
import glob


def get_json_files(root, exclude=None):
    exclude = exclude if exclude else set()

    category_pattern = os.path.join(root, '**/category.json')
    video_pattern = os.path.join(root, '**/videos/*.json')

    category = [path for path in glob.iglob(category_pattern) if path not in exclude]
    video = [path for path in glob.iglob(video_pattern) if path not in exclude]

    return category, video

