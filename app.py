from flask import Flask, request, render_template, send_file, redirect, url_for
from PIL import Image, ImageFont, ImageDraw
import io
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # max 8MB upload

def draw_text_on_image(img, top_text, bottom_text, font_path=None, font_size_ratio=0.08):
    draw = ImageDraw.Draw(img)
    w, h = img.size
    font_size = max(12, int(h * font_size_ratio))
    if font_path and os.path.exists(font_path):
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()

    def draw_centered_text(text, y):
        lines = []
        words = text.split()
        if not words:
            return
        line = words[0]
        for word in words[1:]:
            test = line + " " + word
            # izračun širine besedila z textbbox
            bbox = draw.textbbox((0, 0), test, font=font)
            text_w = bbox[2] - bbox[0]
            if text_w <= w - 20:
                line = test
            else:
                lines.append(line)
                line = word
        lines.append(line)

        cur_y = y
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            x = (w - text_w) / 2
            stroke_width = max(1, int(font_size * 0.06))
            # outline (črno ozadje)
            for ox in range(-stroke_width, stroke_width+1):
                for oy in range(-stroke_width, stroke_width+1):
                    draw.text((x+ox, cur_y+oy), line, font=font, fill="black")
            draw.text((x, cur_y), line, font=font, fill="white")
            cur_y += text_h

    if top_text:
        draw_centered_text(top_text.upper(), 10)
    if bottom_text:
        draw_centered_text(bottom_text.upper(), h - int(h * 0.25))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if 'image' not in request.files:
        return redirect(url_for('index'))
    file = request.files['image']
    top_text = request.form.get('top_text', '')
    bottom_text = request.form.get('bottom_text', '')

    img = Image.open(file.stream).convert('RGB')
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    draw_text_on_image(img, top_text, bottom_text, font_path=font_path)

    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)
    return send_file(buf, mimetype='image/jpeg', download_name='meme.jpg')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
