# Pianoroll

Play a jukebox of songs on your midi-enabled instrument.  Intended to be installed on a Raspberry Pi with a USB to MIDI
connection.  Uses Flask and Celery to serve a web interface and manage the playlist.  Uses mido to read and send midi 
instructions.

## Songs

Includes ~750 of public domain midi tracks from [Kuhmann.com](http://www.kuhmann.com/Yamaha.htm)

## Instructions

Assuming you have a raspberry pi running on a debian image on your local network.  Assumes you have ansible installed locally.

1.  Pull down repo
2.  Update `ansible/vars/common.yml`
3.  Run `ansible-playbook -i hosts deploy.yml`

Log on to your server at `http://raspberrypi.local` tap on a genre to choose 10 random tracks from that folder and play them.