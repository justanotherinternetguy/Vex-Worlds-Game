import pyrealsense2 as rs 

device_number = ""
config = rs.config()

config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
pipe = rs.pipeline()
pipe_ = pipe.start(config)

pipe_.get_stream(rs.stream.color).as_video_stream_profile().get_intrinsics()
