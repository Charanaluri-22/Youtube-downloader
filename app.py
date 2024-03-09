from flask import Flask, render_template, request
from pytube import YouTube
from tkinter import filedialog, Tk
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

        # Open file dialog to select download directory
        root = Tk()
        root.withdraw()  # Hide Tkinter window
        download_dir = filedialog.askdirectory()
        root.destroy()  # Close Tkinter window

        if download_dir:
            # Download the video to the selected directory
            high_stream.download(download_dir)
            return render_template('success.html', message=high_stream.title,download_dir=download_dir)
        else:
            return render_template('error.html', message="No download directory selected.")

    except Exception as e:
        return render_template("error.html", message="Error: " + str(e))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
