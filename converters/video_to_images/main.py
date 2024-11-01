from video_converter import VideoConverter


if __name__ == '__main__':
    converter = VideoConverter('videos/input_video.mp4')
    converter.to_frames()
    #converter.to_frames(fps=24)
    #converter.convert_format('mkv')