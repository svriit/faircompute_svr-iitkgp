from flask import Flask, request, render_template, send_from_directory,url_for,render_template_string,redirect
from pdf2image import convert_from_path
import os
from tempfile import mkdtemp
from werkzeug.utils import secure_filename
import requests
import base64
from flask import jsonify
import json
import shutil

app = Flask(__name__, static_folder='static')
# Function to authenticate user
def authenticate(email, password):
    url = "https://faircompute.com:8000/api/v0/auth/login"
    request_body = {
        "email": email,
        "password": password,
        "version": "V018"
    }
    response = requests.post(url, data=json.dumps(request_body), headers={"Content-Type": "application/json"})
    return response

@app.route('/')
def index():
    login_form = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
    </head>
    <body>
        <section class="container">
            <div class="login-container">
                <div class="circle circle-one"></div>
                <div class="form-container">
                    <img src="https://raw.githubusercontent.com/hicodersofficial/glassmorphism-login-form/master/assets/illustration.png" alt="illustration" class="illustration" />
                    <h1 class="opacity">LOGIN</h1>
                    <form method="post" action="/login">
                        <input type="text" placeholder="USERNAME" name="email" /> <!-- Updated to include 'name' attribute -->
                        <input type="password" placeholder="PASSWORD" name="password" /> <!-- Updated to include 'name' attribute -->
                        <button class="opacity" type="submit">SUBMIT</button>
                    </form>
                    <div class="register-forget opacity">
                        <a href="https://faircompute.com/">REGISTER</a>
                        <a href="https://faircompute.com/">FORGOT PASSWORD</a>
                    </div>
                </div>
                <div class="circle circle-two"></div>
            </div>
            <div class="theme-btn-container"></div>
        </section>
    </body>
    <style>
    :root {
    --background: #1a1a2e;
    --color: #ffffff;
    --primary-color: #0f3460;
}

* {
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    margin: 0;
    box-sizing: border-box;
    font-family: "poppins";
    background: var(--background);
    color: var(--color);
    letter-spacing: 1px;
    transition: background 0.2s ease;
    -webkit-transition: background 0.2s ease;
    -moz-transition: background 0.2s ease;
    -ms-transition: background 0.2s ease;
    -o-transition: background 0.2s ease;
}

a {
    text-decoration: none;
    color: var(--color);
}

h1 {
    font-size: 2.5rem;
}

.container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.login-container {
    position: relative;
    width: 22.2rem;
}
.form-container {
    border: 1px solid hsla(0, 0%, 65%, 0.158);
    box-shadow: 0 0 36px 1px rgba(0, 0, 0, 0.2);
    border-radius: 10px;
    backdrop-filter: blur(20px);
    z-index: 99;
    padding: 2rem;
    -webkit-border-radius: 10px;
    -moz-border-radius: 10px;
    -ms-border-radius: 10px;
    -o-border-radius: 10px;
}

.login-container form input {
    display: block;
    padding: 14.5px;
    width: 100%;
    margin: 2rem 0;
    color: var(--color);
    outline: none;
    background-color: #9191911f;
    border: none;
    border-radius: 5px;
    font-weight: 500;
    letter-spacing: 0.8px;
    font-size: 15px;
    backdrop-filter: blur(15px);
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    -ms-border-radius: 5px;
    -o-border-radius: 5px;
}

.login-container form input:focus {
    box-shadow: 0 0 16px 1px rgba(0, 0, 0, 0.2);
    animation: wobble 0.3s ease-in;
    -webkit-animation: wobble 0.3s ease-in;
}

.login-container form button {
    background-color: var(--primary-color);
    color: var(--color);
    display: block;
    padding: 13px;
    border-radius: 5px;
    outline: none;
    font-size: 18px;
    letter-spacing: 1.5px;
    font-weight: bold;
    width: 100%;
    cursor: pointer;
    margin-bottom: 2rem;
    transition: all 0.1s ease-in-out;
    border: none;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    -ms-border-radius: 5px;
    -o-border-radius: 5px;
    -webkit-transition: all 0.1s ease-in-out;
    -moz-transition: all 0.1s ease-in-out;
    -ms-transition: all 0.1s ease-in-out;
    -o-transition: all 0.1s ease-in-out;
}

.login-container form button:hover {
    box-shadow: 0 0 10px 1px rgba(0, 0, 0, 0.15);
    transform: scale(1.02);
    -webkit-transform: scale(1.02);
    -moz-transform: scale(1.02);
    -ms-transform: scale(1.02);
    -o-transform: scale(1.02);
}

.circle {
    width: 8rem;
    height: 8rem;
    background: var(--primary-color);
    border-radius: 50%;
    -webkit-border-radius: 50%;
    -moz-border-radius: 50%;
    -ms-border-radius: 50%;
    -o-border-radius: 50%;
    position: absolute;
}

.illustration {
    position: absolute;
    top: -14%;
    right: -2px;
    width: 90%;
}

.circle-one {
    top: 0;
    left: 0;
    z-index: -1;
    transform: translate(-45%, -45%);
    -webkit-transform: translate(-45%, -45%);
    -moz-transform: translate(-45%, -45%);
    -ms-transform: translate(-45%, -45%);
    -o-transform: translate(-45%, -45%);
}

.circle-two {
    bottom: 0;
    right: 0;
    z-index: -1;
    transform: translate(45%, 45%);
    -webkit-transform: translate(45%, 45%);
    -moz-transform: translate(45%, 45%);
    -ms-transform: translate(45%, 45%);
    -o-transform: translate(45%, 45%);
}

.register-forget {
    margin: 1rem 0;
    display: flex;
    justify-content: space-between;
}
.opacity {
    opacity: 0.6;
}

.theme-btn-container {
    position: absolute;
    left: 0;
    bottom: 2rem;
}

.theme-btn {
    cursor: pointer;
    transition: all 0.3s ease-in;
}

.theme-btn:hover {
    width: 40px !important;
}

@keyframes wobble {
    0% {
        transform: scale(1.025);
        -webkit-transform: scale(1.025);
        -moz-transform: scale(1.025);
        -ms-transform: scale(1.025);
        -o-transform: scale(1.025);
    }
    25% {
        transform: scale(1);
        -webkit-transform: scale(1);
        -moz-transform: scale(1);
        -ms-transform: scale(1);
        -o-transform: scale(1);
    }
    75% {
        transform: scale(1.025);
        -webkit-transform: scale(1.025);
        -moz-transform: scale(1.025);
        -ms-transform: scale(1.025);
        -o-transform: scale(1.025);
    }
    100% {
        transform: scale(1);
        -webkit-transform: scale(1);
        -moz-transform: scale(1);
        -ms-transform: scale(1);
        -o-transform: scale(1);
    }
}
</style>
<script>
const themes = [
    {
        background: "#1A1A2E",
        color: "#FFFFFF",
        primaryColor: "#0F3460"
    },
    {
        background: "#461220",
        color: "#FFFFFF",
        primaryColor: "#E94560"
    },
    {
        background: "#192A51",
        color: "#FFFFFF",
        primaryColor: "#967AA1"
    },
    {
        background: "#F7B267",
        color: "#000000",
        primaryColor: "#F4845F"
    },
    {
        background: "#F25F5C",
        color: "#000000",
        primaryColor: "#642B36"
    },
    {
        background: "#231F20",
        color: "#FFF",
        primaryColor: "#BB4430"
    }
];

const setTheme = (theme) => {
    const root = document.querySelector(":root");
    root.style.setProperty("--background", theme.background);
    root.style.setProperty("--color", theme.color);
    root.style.setProperty("--primary-color", theme.primaryColor);
    root.style.setProperty("--glass-color", theme.glassColor);
};

const displayThemeButtons = () => {
    const btnContainer = document.querySelector(".theme-btn-container");
    themes.forEach((theme) => {
        const div = document.createElement("div");
        div.className = "theme-btn";
        div.style.cssText = `background: ${theme.background}; width: 25px; height: 25px`;
        btnContainer.appendChild(div);
        div.addEventListener("click", () => setTheme(theme));
    });
};

displayThemeButtons();

</script>
    </html>
    """
    return render_template_string(login_form)

@app.route('/login', methods=['POST'])
def login():
    # Here we handle the login form submission
    email = request.form['email']
    password = request.form['password']
    response = authenticate(email, password)
    if response.status_code == 200:
        # Redirect user to another page, maybe home
        return redirect(url_for('home'))
    else:
        # Instead of using flash, you could return an error message directly in the response
        # or redirect the user to the login page with an error flag and handle it there.
        return redirect(url_for('index'))  # Redirect to login page without an error message
# Temporary directory for storing uploaded PDFs and converted images
UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_pdf():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return 'No file part'
        file = request.files['pdf_file']
        if file.filename == '':
            return 'No selected file'
        
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(pdf_path)
        
        images = convert_from_path(pdf_path, dpi=96)
        image_filenames = []
        for i, image in enumerate(images):
            image_filename = f'image_{i}.jpg'
            image_path = os.path.join(UPLOAD_FOLDER, image_filename)
            image.save(image_path)
            image_filenames.append(image_filename)
        # Render a template displaying all the images side by side
        # return render_template('images.html', image_filenames=image_filenames)
        print("sdahbd",image_filenames)
        return jsonify({'image_filenames': image_filenames})
    
    # Render the upload form
    return '''
    <!doctype html>
    <title>Upload PDF</title>
    <h1>Upload PDF to convert to images</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=pdf_file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print()
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/api/generate', methods=['POST'])
def generate_api_call():
    data = request.json
    selected_image_filename = data.get('selectedImage')
    user_input = data.get('userInput')
    
    # Path to the selected image
    image_path = os.path.join(UPLOAD_FOLDER, selected_image_filename)
    
    # Convert the image to a base64 string
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Prepare the payload for the external API
    payload = {
        "model": "llava:7b-v1.6-mistral-q5_K_M",
        "prompt": user_input,
        "stream": False,
        "images": [base64_image]
    }
    
    # API endpoint
    api_endpoint = "http://8.12.5.48:11434/api/generate"
    
    # Make the API call
    response = requests.post(api_endpoint, json=payload)
    
    if response.status_code == 200:
        # Process the response as needed
        return response.json()  
    else:
        return {'error': 'API call failed'}, 500
    
@app.route('/images', methods=['GET', 'POST'])
def home():
    return render_template('images.html')

@app.route('/clear_uploads', methods=['POST'])
def clear_uploads():
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'success': 'Uploads cleared'}), 200

if __name__ == '__main__':
    app.run(debug=True)