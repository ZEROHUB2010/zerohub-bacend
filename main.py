import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)  # Иҷозат додан ба GitHub Pages барои фиристодани дархост

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "Server is running!"}), 200

@app.route('/api/get-download-link', methods=['GET'])
def get_download_link():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': 'URL лозим аст'}), 400

    # Танзимоти yt-dlp барои гирифтани линкҳои мустақим
    ydl_opts = {
        'format': 'best',  # Видеои босифат бо аудио
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            return jsonify({
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'duration': info.get('duration_string', 'HD'),
                'download_url': info.get('url'),  # Линки мустақими файл!
                'ext': info.get('ext', 'mp4')
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
