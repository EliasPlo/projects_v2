import moviepy.editor as mp
import cv2
import os

# Menu for the video editing tool
def menu():
    print("\n--- Video Editing Tool ---")
    print("1. Cut a video")
    print("2. Combine videos")
    print("3. Adjust video speed")
    print("4. Mute video")
    print("5. Convert video format")
    print("6. Exit")

# Cut a video
def cut_video(input_file, start_time, end_time, output_file):
    video = mp.VideoFileClip(input_file)
    cut_video = video.subclip(start_time, end_time)
    cut_video.write_videofile(output_file, codec="libx264")
    print(f"Video saved to {output_file}")

# Combine multiple videos
def combine_videos(video_files, output_file):
    clips = [mp.VideoFileClip(video) for video in video_files]
    combined = mp.concatenate_videoclips(clips)
    combined.write_videofile(output_file, codec="libx264")
    print(f"Combined video saved to {output_file}")

# Adjust video speed
def adjust_speed(input_file, speed_factor, output_file):
    video = mp.VideoFileClip(input_file)
    modified = video.fx(mp.vfx.speedx, speed_factor)
    modified.write_videofile(output_file, codec="libx264")
    print(f"Video with adjusted speed saved to {output_file}")

# Mute video
def mute_video(input_file, output_file):
    video = mp.VideoFileClip(input_file)
    muted = video.without_audio()
    muted.write_videofile(output_file, codec="libx264")
    print(f"Muted video saved to {output_file}")

# Convert video format
def convert_format(input_file, output_file):
    video = mp.VideoFileClip(input_file)
    video.write_videofile(output_file, codec="libx264")
    print(f"Video converted and saved to {output_file}")

# Main function
def main():
    while True:
        menu()
        choice = input("Select an option: ")
        
        if choice == "1":
            input_file = input("Enter the input video file path: ")
            start_time = int(input("Enter the start time in seconds: "))
            end_time = int(input("Enter the end time in seconds: "))
            output_file = input("Enter the output file name (e.g., output.mp4): ")
            cut_video(input_file, start_time, end_time, output_file)

        elif choice == "2":
            video_count = int(input("How many videos do you want to combine? "))
            video_files = [input(f"Enter path for video {i+1}: ") for i in range(video_count)]
            output_file = input("Enter the output file name (e.g., combined.mp4): ")
            combine_videos(video_files, output_file)

        elif choice == "3":
            input_file = input("Enter the input video file path: ")
            speed_factor = float(input("Enter the speed factor (e.g., 2.0 for double speed, 0.5 for half speed): "))
            output_file = input("Enter the output file name (e.g., speed_adjusted.mp4): ")
            adjust_speed(input_file, speed_factor, output_file)

        elif choice == "4":
            input_file = input("Enter the input video file path: ")
            output_file = input("Enter the output file name (e.g., muted.mp4): ")
            mute_video(input_file, output_file)

        elif choice == "5":
            input_file = input("Enter the input video file path: ")
            output_file = input("Enter the output file name with desired format (e.g., converted.avi): ")
            convert_format(input_file, output_file)

        elif choice == "6":
            print("Exiting the tool. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
