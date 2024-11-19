AUDIO_OPTIONS = {
            "format": ["mp3", "mov", "avi", "mkv", "flv", "webm", "ogg", "wmv"],
            "bit_rate": ["32K", "64K", "96K", "128K", "192K", "256K", "320K"],
            "audio_channels": ['1', '2', '3', '4', '5' ,'6','7' ,'8'],
            "sample_rate": ['8000', '22050' , '44100' , '48000' , '96000', '192000'],
            "volume": ['0.5', '1.5'],
            "speed_minimum": 0.5,
            "speed_maximum": 2.0
        }

IMAGE_OPTIONS = {
    "filter" : ["BLUR", "CONTOUR", "DETAIL", "EDGE_ENHANCE", "EDGE_ENHANCE_MORE", "EMBOSS", 
            "FIND_EDGES", "SHARPEN", "SMOOTH", "SMOOTH_MORE", "GRAYSCALE"],
    "extension" : ['jpg', 'jpeg', 'png', 'gif'],
    "resize_type": ["THUMBNAIL", "COVER", "FIT", "PAD"]
}

VIDEO_OPTIONS = {
            "format": ["mp4", "mov", "avi", "mkv", "flv", "webm", "ogg", "wmv"],
            "vcodec": ["libx264", "libx265", "mpeg4", "vp8", "vp9", "prores", "huffyuv", "hevc_nvenc"],
            "acodec": ["aac", "mp3", "opus", "ac3", "pcm_s16le", "vorbis"],
            "audio_channels": ['1', '2', '4', '6', '8']
        }