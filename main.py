from flask import Flask, render_template, Response
from camera import VideoCamera
from camera2 import VideoCamera2

app = Flask(__name__)

camera = None 
camera2 = None 

def get_camera_instance():
    global camera
    if camera is None:
        camera = VideoCamera()
    return camera

def get_camera_instance2():
    global camera2
    if camera2 is None:
        camera2 = VideoCamera2()
    return camera2

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/biceps')
def biceps():
    global camera2
    if camera2 is None:
        camera2 = VideoCamera2()
    return render_template('bicep.html')

@app.route('/pushup')
def pushup():
    global camera
    if camera is None:
        camera = VideoCamera()
    return render_template('pushup.html')

def gen(camera):
    while True:
        frame = camera.get_pushup()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-type:image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
def gen2(camera2):
    while True:
        frame = camera2.get_bicep()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-type:image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/feed')
def feed():
    return Response(gen(get_camera_instance()),
                    mimetype='multipart/x-mixed-replace;boundary=frame')

@app.route('/bicep')
def bicep():
    return Response(gen2(get_camera_instance2()),
                    mimetype='multipart/x-mixed-replace;boundary=frame')

@app.route('/count')
def final_count():
    global camera
    if camera is not None:
        camera.__del__()
        count = camera.get_count() 
        camera = None
        return render_template('count.html', count=count)
    return render_template('count.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
