# Source Video as a Stream

You can use any video-file or video-device 
as an input for the Shot Detector.
But in some cases it is required to use on-the-fly video stream.

You can get video-stream from third-party source or generate 
it yourself. There are several ways to generate your own input video 
stream:

* from a file;
* from your camera;
* from your desktop;
* from a virtual device.

More over you can implement it with different schemes of streaming:

* point to point streaming;
* streaming with server (`ffserver`).


## Point to point

This is the simplest way to reproduce on-the-fly video stream.
In this case you generate stream only for one reader.
If you use your stream for the Shot Detector,
you cannot check it without stopping the Shot Detector.
But in this stream embodiment you wont deal with latency.

### SDP-file and RTP-stream 

In this case we use [RTP Streaming Protocol]
(https://en.wikipedia.org/wiki/Real-time_Transport_Protocol). 
The main limitation of it is that only one stream supported 
in the RTP muxer. So you can stream only video without audio
or audio without video.

#### File Streaming

1. Create a SDP-file and RTP-stream  with `ffmpeg`. 
    For a file stream it looks like this:
   
        ffmpeg -re -i input-file.mp4 -an -f rtp rtp://127.0.0.1:1236 > file-stream.sdp

    Where:
    
    * `-re ` — is a flag that makes ffmpeg read input at native frame 
    rate. In this case it is used to simulate a stream from a device.
    Without this flag, your stream will be handled as a simple file.
    It is required only if you work with static file but not real stream.
    * `-i input-file.mp4` — is a name of input file.
    * `-an` — is a flag that makes ffmpeg ignore audio streams.
    The reason of this flag is that RTP doesn't support more than one 
    stream. Moreover, if your file contains several video streams,
    your should choose one and remove odd video streams.
    * `-f rtp` — is an output format — [RTP]
    (https://en.wikipedia.org/wiki/Real-time_Transport_Protocol).
    * `rtp://127.0.0.1:1234` — an address for receiving stream of 
    virtual device.
    * `./file-stream.sdp` — is a is a [stream session description file]
    (https://en.wikipedia.org/wiki/Session_Description_Protocol). 
    
2. Check the `./file-stream.sdp`. In this case it contains following text:
    
        SDP:
        v=0
        o=- 0 0 IN IP4 127.0.0.1
        s=No Name
        c=IN IP4 127.0.0.1
        t=0 0
        a=tool:libavformat 55.33.1000
        m=video 1234 RTP/AVP 96
        b=AS:2000
        a=rtpmap:96 MP4V-ES/90000
        a=fmtp:96 profile-level-id=1

3. Check the stream. Run `ffplay` with `./file-stream.sdp` as an arguments.
        
        ffplay ./file-stream.sdp

    You get a window with video from your file-stream.
    
    * More over you can use any another player that supports RTP.
        For example:
    
            mplayer ./file-stream.sdp
    
4. Stop `ffplay` and then use `./file-stream.sdp` file name 
    as input URI for the Shot Detector
    
**Note:** RTP uses UDP, so the receiver can start up any time, but
you can get packet loss.

#### Virtual Device


1. Create a SDP-file and RTP-stream  with `ffmpeg`. 
    For a virtual device it looks like this:
    
        ffmpeg -f lavfi -i mandelbrot -f rtp rtp://127.0.0.1:1234 > virtual-device.sdp 

    Where:
    
    * `-f lavfi` — is format of libavfilter input [virtual device]
        (https://www.ffmpeg.org/ffmpeg-devices.html#lavfi).
        This input device reads data from 
        the open output pads of a libavfilter filtergraph.
    * `-i mandelbrot` — is a filter that draws the [Mandelbrot set]
    (https://en.wikipedia.org/wiki/Mandelbrot_set).
    Check [Fancy Filtering Examples]
    (https://trac.ffmpeg.org/wiki/FancyFilteringExamples#Video)
    in FFmpeg documentaion for another filter types.
    * `-f rtp` — is an output format — [RTP]
    (https://en.wikipedia.org/wiki/Real-time_Transport_Protocol).
    * `rtp://127.0.0.1:1234` — an address for receiving stream of 
    virtual device.
    * `./virtual-device.sdp` — is a is a [stream session description file]
    (https://en.wikipedia.org/wiki/Session_Description_Protocol). 
    
2. Use `virtual-device.sdp` as discussed above.

#### Camera

Create a SDP-file and RTP-stream  with `ffmpeg`. 
For a camera it looks like this:

    ffmpeg -f v4l2 -i /dev/video0 -f rtp rtp://127.0.0.1:1234 > camera.sdp

Where:

* `-f v4l2` — is an input device-format for a camera. 
The full name of it is — [video4linux2]
(https://www.ffmpeg.org/ffmpeg-devices.html#video4linux2_002c-v4l2)
*It works only for linux.* For another systems, please, 
check this page: [FFmpeg Streaming Guide]
(https://trac.ffmpeg.org/wiki/StreamingGuide "Streaming Guide")
* `-i /dev/video0` — is a path to device.
* `-f rtp` — is an output format — [RTP]
(https://en.wikipedia.org/wiki/Real-time_Transport_Protocol).
* `rtp://127.0.0.1:1234` — an address for receiving camera's stream.
* `./camera.sdp` — is a file with a description of your 
[stream session](https://en.wikipedia.org/wiki/Session_Description_Protocol). 

After that use `camera.sdp` as discussed above.

#### Desktop Capturing

For a Linux display ffmpeg-command looks like this:

    ffmpeg -f x11grab -video_size wxga  -i :0.0  -f rtp rtp://127.0.0.1:1234 > desktop.sdp

Where:

* `-f x11grab` — is an input format for a [X11-display]
(https://www.ffmpeg.org/ffmpeg-devices.html#x11grab). 
* `-video_size wxga` — size of your display. In this case we use the 
full size of desktop. Check [FFmpeg Capture/Desktop]
(https://trac.ffmpeg.org/wiki/Capture/Desktop) page for other options
* `-i :0.0` — is a desktop name.
* `-f rtp` — is an output format 
* `rtp://127.0.0.1:1234` — an address for receiving camera's stream.
* `./desktop.sdp` — is a stream session description file.

After that use `desktop.sdp` as discussed above.

### MPEG-TS

With [MPEG-TS](https://en.wikipedia.org/wiki/MPEG_transport_stream) you 
can generate both and audio and video.

#### MPEG-TS UDP Streaming

In this case we use [UDP]
(https://en.wikipedia.org/wiki/User_Datagram_Protocol).
So, you still can get packet loss.
They are likely to reveal if you stream via Internet.

Here is example for a camera.
For another devices they are the same.

1. Start `ffmpeg` to generate **MPEG-TS** stream via udp.
    
        ffmpeg -f v4l2 -i /dev/video0  -f mpegts udp://127.0.0.1:1234

    Where:
    
    * `-f v4l2` — is an input device-format for a camera. 
    It works only for linux. For another systems, please, 
    check this page: [FFmpeg Streaming Guide]
    (https://trac.ffmpeg.org/wiki/StreamingGuide "Streaming Guide")
    * `-i /dev/video0` — is a path to device.
    * `-f mpegts` — is an output format — MPEG transport stream.
    * `udp://127.0.0.1:1234` — an address for receiving camera's stream.

2. Check it with `ffplay`:

    ffplay  -fflags nobuffer  udp://127.0.0.1:1234
    
    Where:
    
    * `-fflags nobuffer` — is a flag that makes ffplay don't cache 
    input stream. We set it to reduce latency.
    
3. Use `udp://127.0.0.1:1234` as input video URI for the Shot Detector.   

More over, you can start `ffmpeg` and the Shot Detector in any order.

**Note:** The time in the Shot Detector is a time of a video stream.

#### MPEG-TS TCP streaming

Another option is to use TCP connections for MPEG-TS streaming.
In this case you don't get packet loss.
But you should guarantee that a reader will be started before
a writer. So, reader become a server and writer become a client.

For example:

1. Start `ffplay` as a server

        ffplay  -fflags nobuffer  tcp://127.0.0.1:1234?listen

    Where:
    
    * `-fflags nobuffer` — is a flag that makes ffplay don't cache 
    input stream. We set it to reduce latency.
    * `tcp://127.0.0.1:1234?listen` — is a host for sending 
    camera's stream whith `listen` option.
    A writer should send stream to `tcp://127.0.0.1:1234`.
     
     
2. Start `ffmpeg` as a client

        ffmpeg -f v4l2 -i /dev/video0  -f mpegts tcp://127.0.0.1:1234

    Where
    
    * `-f v4l2` — is an input device-format for a camera. 
    It works only for linux. For another systems, please, 
    check this page: [FFmpeg Streaming Guide]
    (https://trac.ffmpeg.org/wiki/StreamingGuide "Streaming Guide")
    * `-i /dev/video0` — is a path to device.
    * `-f mpegts` — is an output format — MPEG transport stream.
    * `tcp://127.0.0.1:1234` — an address for sending camera's stream.


So, you can pass `tcp://127.0.0.1:1234?listen` as an input video URI 
for the Shot Detector but you should start it before `ffmpeg`.


## Streaming Severver


### For camera :

    /usr/bin/ffmpeg -f v4l2 -s 640x480 -r 25 -i /dev/video0 -f alsa -i hw:0 -tune zerolatency -b 900k  http://localhost:8090/feed1.ffm
 
 
### For screen:
 
    /usr/bin/ffmpeg -threads 0  -f x11grab -s wxga -r 25 -i :0.0 -f alsa  -i hw:0 -tune zerolatency -b 900k  http://localhost:8090/feed1.ffm



### FFserver Config example:
     
```config
Port 8090
BindAddress 0.0.0.0
MaxHTTPConnections 2000
MaxClients 1000
MaxBandwidth 1000
CustomLog -
#NoDaemon

<Feed feed1.ffm>
    File /tmp/feed1.ffm
    FileMaxSize 200K
    ACL allow 127.0.0.1
</Feed>

# if you want to use mpegts format instead of flv
# then change "live.flv" to "live.ts"
# and also change "Format flv" to "Format mpegts"
<Stream live.flv>
    Format flv
    Feed feed1.ffm

    VideoCodec libx264
    VideoFrameRate 30
    VideoBitRate 512
    VideoSize 320x240
    AVOptionVideo crf 23
    AVOptionVideo preset medium
    # for more info on crf/preset options, type: x264 --help
    AVOptionVideo flags +global_header

    AudioCodec aac
    Strict -2
    AudioBitRate 128
    AudioChannels 2
    AudioSampleRate 44100
    AVOptionAudio flags +global_header
</Stream>

    
<Stream live.ogg>
    Format ogg
    Feed feed1.ffm

    VideoCodec libtheora
    VideoFrameRate 24
    VideoBitRate 512
    VideoSize 320x240
    VideoQMin 1
    VideoQMax 31
    VideoGopSize 12
    Preroll 0
    AVOptionVideo flags +global_header

    AudioCodec libvorbis
    AudioBitRate 64
    AudioChannels 2
    AudioSampleRate 44100
    AVOptionAudio flags +global_header
</Stream>


##################################################################
# Special streams
##################################################################
<Stream stat.html>
    Format status
    # Only allow local people to get the status
    ACL allow localhost
    ACL allow 192.168.0.0 192.168.255.255
</Stream>

# Redirect index.html to the appropriate site
<Redirect index.html>
    URL http://www.ffmpeg.org/
</Redirect>
##################################################################
```


### Check

    smplayer http://localhost:8090/live.flv 


