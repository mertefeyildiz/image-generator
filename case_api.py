from flask import Flask, request, send_file, render_template
from diffusers import DiffusionPipeline
from PIL import Image, ImageDraw, ImageFont
import io
import os
import torch
import random

app = Flask(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1-unclip-small")
pipe.to(device)



input_image_path = 'output_png_image.png'
output_image_path = 'output_png_image.png'
# Görüntüyü PNG formatına çevir
im = Image.open(input_image_path).convert("RGBA")
im.save(output_image_path)

#############################################################



image = Image.new("RGB", (300, 200), (255, 255, 255))
draw = ImageDraw.Draw(image)
xy = [50, 0,46,15]
bar_height = 15
corner_radius = 10
rgb_color=(52, 152, 219)

def modify_random_area(image, rgb_color):
    # Rasgele bir 200x200 piksel alan seç
    width, height = image.size
    x = random.randint(0, width - 200)
    y = random.randint(0, height - 200)
    box = (x, y, x + 200, y + 200)

    # Seçilen alan içindeki piksellerin %20'sini belirtilen renk koduyla değiştir
    selected_area = image.crop(box)
    selected_pixels = list(selected_area.getdata())
    num_pixels_to_change = int(0.2 * len(selected_pixels))  # %20'sini değiştirmek için gereken piksel sayısı
    for _ in range(num_pixels_to_change):
        index = random.randint(0, len(selected_pixels) - 1)
        selected_pixels[index] = rgb_color
    selected_area.putdata(selected_pixels)
    image.paste(selected_area, box)
    return image



from PIL import Image, ImageDraw

def rounded_rectangle(draw, xy, corner_radius, fill=None):
    upper_left = xy[0]
    lower_right = xy[1]

    # Draw main rectangle
    draw.rectangle([upper_left, lower_right], fill=fill)

    # Draw four rounded corners
    draw.pieslice([upper_left, (upper_left[0] + corner_radius * 2, upper_left[1] + corner_radius * 2)],
                  180, 270, fill=fill)
    draw.pieslice([(lower_right[0] - corner_radius * 2, upper_left[1]),
                   lower_right], 270, 360, fill=fill)
    draw.pieslice([(upper_left[0], lower_right[1] - corner_radius * 2),
                   (upper_left[0] + corner_radius * 2, lower_right[1])], 90, 180, fill=fill)
    draw.pieslice([(lower_right[0] - corner_radius * 2, lower_right[1] - corner_radius * 2),
                   lower_right], 0, 90, fill=fill)

    # Draw straight parts of the border
    draw.rectangle([upper_left[0] + corner_radius, upper_left[1], lower_right[0] - corner_radius, upper_left[1] + corner_radius], fill=fill)
    draw.rectangle([upper_left[0], upper_left[1] + corner_radius, upper_left[0] + corner_radius, lower_right[1] - corner_radius], fill=fill)
    draw.rectangle([lower_right[0] - corner_radius, upper_left[1] + corner_radius, lower_right[0], lower_right[1] - corner_radius], fill=fill)
    draw.rectangle([upper_left[0] + corner_radius, lower_right[1] - corner_radius, lower_right[0] - corner_radius, lower_right[1]], fill=fill)

###############################################################

rad= 80
def add_corners(im, rad):
    # Daire şeklinde bir maske oluştur
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)

    # Görüntünün boyutunu al
    w, h = im.size

    # Daire maskesini kullanarak köşelere ekleme yap
    alpha = Image.new('L', im.size, 255)
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))

    # Görüntünün alfa kanalını ayarla
    im.putalpha(alpha)
    return im



@app.route('/')
def index():
    return render_template('index3.html')

@app.route('/generate-image', methods=['POST'])


def generate_image():

    if 'file' not in request.files or 'logo' not in request.files:
        return render_template('index3.html', error='No file part')

    file = request.files['file']
    logo_file = request.files['logo']
    
    if file.filename == '' or logo_file.filename == '':
        return render_template('index3.html', error='No selected file')

    prompt = request.form.get('prompt')
    hex_color = request.form.get('color')
    punchline = request.form.get('punchline')
    button_text = request.form.get('button_text')
    button_punchline_color = request.form.get('button_color')


    image = Image.open(file.stream).convert("RGB")
    logo = Image.open(logo_file.stream).convert("RGBA")
    
    # Logoyu 4'te 1 boyutuna getir
    #logo.thumbnail((logo.width // 4, logo.height // 4))
    hex_color = hex_color.lstrip("#")  # Başındaki # işaretini kaldır
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

   
    # Görüntüyü belirli bir boyuta dönüştür
    target_size = (720, 720)
    image = image.resize(target_size, Image.ANTIALIAS)
    width, height = image.size

    image =  modify_random_area(image, rgb_color)

    with torch.no_grad():
        output_image = pipe(prompt=prompt.format(hex_color=hex_color), image=image).images[0]
    #output_image = pipe(prompt=prompt.format(hex_color=hex_color),  image=image).images[0]
    # Beyaz arkaplan oluştur (en ve boy 3 katı büyüklüğünde)
    
    output_image = output_image.convert("RGBA")
    output_image = add_corners(output_image, 80)
    output_image.save('500x5003.png')
    
    input_image_path = '500x5003.png'
    output_image2 = Image.open(input_image_path).convert("RGBA")
    
    background = Image.new('RGB', (output_image2.width * int(2.5), output_image2.height * int(2.5)), 'white')
    logo.thumbnail((output_image2.width // 4, output_image2.height // 4))
    # Beyaz arkaplanın ortasına görüntüyü yerleştir (ortalayarak)
    offset = ((background.width - output_image2.width) // 2, int(((background.height - output_image2.height) // 2) - 40 ))
    background.paste(output_image2, offset, mask = output_image2)

    # Logoyu en tepede ve ortada yapıştır
    offset_logo = (int((background.width - logo.width) // 2), 70 ) #int(((output_image.height // 4)))
    background.paste(logo, offset_logo)

    # Punchline'ı görüntünün alt sınırına yerleştir
    draw = ImageDraw.Draw(background)
    font_punch = ImageFont.truetype("arial.ttf", 120)  
    text_width, text_height = draw.textsize(punchline, font_punch)
    text_position = ((background.width - text_width) // 2, background.height - text_height - (output_image.height * 0.35))
    draw.text(text_position, punchline, font=font_punch, fill=button_punchline_color)
    

    draw = ImageDraw.Draw(background)
    #bar_height=15
    # Top bar


    # Belirtilen renk koduyla görüntüyü doldur
    hex_color = button_punchline_color.lstrip("#")  # Başındaki # işaretini kaldır
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    genislik = 1436
    yukseklik = 15
    image = Image.new("RGBA", (genislik, yukseklik), rgb_color)
    iamge = add_corners(image, 40)
    image.save("output_image_line2.png", format="PNG")
    offset = (50, 0 )
    background.paste(iamge, offset, mask = iamge)
    
    flipped_image = image.rotate(180)

    # Yerleştirme konumunu belirle
    offset = (50, background.height - yukseklik)
    
    # Görüntüyü arka plana ekleyerek mask kullan
    background.paste(flipped_image, offset, mask=flipped_image)

    font_button = ImageFont.truetype("arial.ttf", 50)
    button_width, button_height = draw.textsize(button_text, font_button)
    button_position = ((background.width - button_width) // 2, background.height - button_height - (output_image.height * 0.15))
    
    # Yuvarlanmış kenarlı dikdörtgen çizimi
    x, y = button_position
    width, height = button_width , button_height + 20
    radius = 10
    
    draw.rectangle(
        [(x - 20, y + radius), (x + width + 20, y + height - radius)],
        fill=button_punchline_color
    )
    draw.rectangle(
        [(x + radius - 20, y), (x + width - radius + 20, y + height)],
        fill=button_punchline_color
    )
    draw.pieslice(
        (x - 20, y, x + 2 * radius - 20, y + 2 * radius),
        180,
        270,
        fill=button_punchline_color
    )
    draw.pieslice(
        (x + width - 2 * radius + 20, y, x + width + 20, y + 2 * radius),
        270,
        360,
        fill=button_punchline_color
    )
    draw.pieslice(
        (x - 20, y + height - 2 * radius, x + 2 * radius - 20, y + height),
        90,
        180,
        fill=button_punchline_color
    )
    draw.pieslice(
        (x + width - 2 * radius + 20, y + height - 2 * radius, x + width + 20, y + height),
        0,
        90,
        fill=button_punchline_color
    )
    
    # Buton metnini çizme
    draw.text((x, y), button_text, font=font_button, fill='white')    # Modifiye edilmiş arka plan görüntüsünü kaydet
    output_path = os.path.join(app.root_path, 'output_template.png')
    background.save(output_path)

    # Görüntüyü ekrana bastır
    byte_io = io.BytesIO()
    background.save(byte_io, 'PNG')
    byte_io.seek(0)

    return send_file(byte_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=False, port=80, threaded=True) #





