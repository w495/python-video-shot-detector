




## FFmpeg command example:

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


