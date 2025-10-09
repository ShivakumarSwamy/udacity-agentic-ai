import os

from dotenv import load_dotenv

load_dotenv()


def main():
    chapter_name = os.environ.get("CHAPTER")
    lesson_name = os.environ.get("LESSON")
    sub_folders = [
        "exercises",
        "notes",
        "quizzes"
    ]

    base_path = os.path.join(chapter_name, lesson_name)
    os.makedirs(base_path, exist_ok=True)

    print(f"created directory: {base_path}")

    for folder in sub_folders:
        sub_folder_path = os.path.join(base_path, folder)
        os.makedirs(sub_folder_path, exist_ok=True)
        print(f"created sub folder: {sub_folder_path}")


if __name__ == '__main__':
    main()
