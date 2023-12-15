# RTL-SDR (FM/HD) Radio Streaming to Icecast

This [docker-compose.yml](/docker-compose.yml) sample provides all of the services required to use a [RTL-SDR usb dongle](https://www.rtl-sdr.com/about-rtl-sdr/) to tune into a FM HD radio -- or any analogue signal supported by [ShinySDR](https://shinysdr.switchb.org/) (AM, FM, SSB, CW) -- and generate a streaming endpoint that can be consumed by a media player.

# How It Works

#### Accessing RTL-SDR device 

Your host machine passes the RTL-SDR device to an [rtl_tcp server](https://manpages.ubuntu.com/manpages/lunar/en/man1/rtl_tcp.1.html) ([dockerized example](https://hub.docker.com/r/kosdk/rtl-tcp)) which is accessible over TCP for tuning and getting signal.

#### Tuner uses Signal

**One of the available tuners**, [nrsc5](https://github.com/FoxxMD/nrsc5-rtlsdr-icecast) for HD FM or [ShinySDR](https://github.com/jeffersonjhunt/shinysdr-docker) for general use, accesses the rtl_tcp server and tunes/converts the analogue signal into uncompressed, digital audio.

**NOTE:** Only one tuner can be used at a time!

#### Convert and stream to Icecast

`ffmpeg` is used to convert uncompressed audio into an mp3/ogg stream which is then streamed to [icecast](https://github.com/jee-r/docker-icecast) at the URL of your choosing. The URL can then be directly accessed by multiple clients to get streaming audio.

#### (Optional) Scheduled download of stream

[yt-dlp](https://github.com/yt-dlp/yt-dlp) is [used alongside cron](https://github.com/FoxxMD/ytdl-cron-docker) enabling you to schedule saving the stream at preset times and for an arbitrary duration.

# Usage

## Getting RTL-SDR USB Path

You must determine the correct USB path to pass to the **rtl_tcp** service in order for it to access your radio device.

Run `lsusb` to get a list of USB devices attached to your host. It will look like this:

```
$ lsusb
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 002: ID 8087:0032 Intel Corp. AX210 Bluetooth
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
...
Bus 005 Device 006: ID 0bda:2838 Realtek Semiconductor Corp. RTL2838 DVB-T
Bus 006 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
```

Look for your device, it usually has **RTL** or **DVB-T** in the name. Use the `Bus` and `Device` identifiers to build the path to your usb device. EX:

> Bus **005** Device **006**: ID 0bda:2838 Realtek Semiconductor Corp. RTL2838 DVB-T

```
/dev/bus/usb/005/006
```
This is used in [docker-compose.yml](/docker-compose.yml) under **rtl_tcp** `devices`

## Choosing a Tuner

**YOU CAN ONLY USE ONE TUNER AT A TIME.**

Either comment out the tuner block you do not want in `docker-compose.yml` or make sure you specify which services to bring `up` when running `docker-compose`.

### nrsc5

[nrsc5](https://github.com/theori-io/nrsc5) is used to convert digital (HD) FM radio to a usable audio signal. This audio will have (almost) zero static and be a higher quality than the analogue audio signal for normal FM radio.

### ShinySDR

[ShinySDR](https://shinysdr.switchb.org/) is a general purpose radio receiver with a web-based interface. It can play most analogue signals and decode many common digital signals. **It cannot decode HD radio at this time.**

The audio sent to Icecast will be whatever you have tuned ShinySDR to using the interface.

## Using Icecast

Reference [docker-compose.yml](/docker-compose.yml) to set the URL the tuners send audio to:

* nrsc5 => `ICECAST_URL=icecast:8000/myradio`
* shiny => `...icecast://source:hackme@icecast:8000/myradio`

Change `myradio` to whatever you want the stream to be accessible at. The stream will be available at `http://localhost:8000/myradio` (or whatever you set)

## (Optional) Scheduled stream downloads

If your docker installation is on a **linux host** you must set [PUID and PGID](https://docs.linuxserver.io/general/understanding-puid-and-pgid/) environmental variables in the `icecast_ytdl` service in [docker-compose.yml](/docker-compose.yml) or the files generated will likely not be accessible.

To set the schedule edit [/config/ytdl/crontabs/abc](/config/ytdl/crontabs/abc):

* set the [cron expression](https://crontab.guru/)
* edit downloading length `--download-sections "*0-20"` in seconds IE `*0-20` = save the first two seconds of the stream