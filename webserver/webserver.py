from flask import Flask, render_template, redirect, request
import mido
from mido import MidiFile, tempo2bpm, Message
from time import sleep
import os
from celery import Celery

celery = Celery(broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

rootDir = '../songs/'

app = Flask(__name__)


@app.route("/")
def songs():
    dirs = os.walk(rootDir)
    return render_template('songs.html', dirs=dirs)


@celery.task(name='playsong')
def playsong(filename):
    portname = 'USB Midi MIDI 1'
    midifile = MidiFile(filename)
    with mido.open_output(portname) as output:
        output.reset()
        for message in midifile.play():
            if isinstance(message, Message):
                output.send(message)
            elif message.type == 'set_tempo':
                print('Tempo changed to {:.1f} BPM.'.format(tempo2bpm(message.tempo)))
        output.reset()


@app.route("/play")
def play():
    filename = request.args.get('filename')
    playsong.delay(filename)
    return redirect('/')


@app.route('/remove')
def remove():
    taskid = request.args.get('taskid')
    celery.control.revoke(taskid, terminate=True)
    return redirect('/')


@app.route('/playlist')
def playlist():
    inspect = celery.control.inspect()
    tasks = []
    active = inspect.active()
    if active:
        keys = active.keys()
        for key in keys:
            try:
                tasks.append(active[key][0])
            except IndexError:
                pass
    return render_template('playlist.html', tasks=tasks)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
