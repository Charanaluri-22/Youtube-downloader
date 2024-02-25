from flask import Flask, render_template, request
from pytube import YouTube
from tkinter import filedialog,Tk
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']
    try:
        yt = YouTube(video_url)
        high_stream = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
        print(high_stream.title)
        high_stream.download()
        return render_template('success.html',message=high_stream.title)
    except Exception as e:
        return render_template("error.html",message="Error: "+str(e))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
def open_file_dialog():
    filepath = filedialog.askopenfilename()
    if filepath:
        print("Selected file:", filepath)
    else:
        print("No file selected")

if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    app.run(debug=True)
