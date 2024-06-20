from flask import Flask, request, jsonify, render_template_string
from pyngrok import ngrok

# Set your ngrok authtoken (replace "YOUR_NGROK_AUTH_TOKEN" with your actual token)
ngrok.set_auth_token("YOUR_NGROK_AUTH_TOKEN")

# Define the alphabet and mappings
alphabet = "abcdefghijklmnopqrstuvwxyz "
letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))

# Define the decryption function


def decrypt(cipher, key):
    decrypted = ""
    split_encrypted = [
        cipher[i: i + len(key)] for i in range(0, len(cipher), len(key))
    ]

    for each_split in split_encrypted:
        i = 0
        for letter in each_split:
            number = (letter_to_index[letter] -
                      letter_to_index[key[i]]) % len(alphabet)
            decrypted += index_to_letter[number]
            i += 1

    return decrypted


# Set up the Flask app
app = Flask(__name__)

# Define the home route


@app.route('/')
def home():
    # HTML form for decryption
    html_form = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Decrypt Message</title>
        <style>
            body {
                background-color: black;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 20px;
            }
            #formContainer {
                display: inline-block;
                text-align: left;
            }
        </style>
    </head>
    <body>
        <h2>Decrypt Message</h2>
        <div id="formContainer">
            <form id="decryptForm" method="post" action="/decrypt">
                <h3>Decrypt Message</h3>
                <label for="cipher">Cipher:</label>
                <input type="text" id="cipher" name="cipher"><br><br>
                <label for="key">Key:</label>
                <input type="text" id="key" name="key"><br><br>
                <button type="button" onclick="submitForm()">Decrypt</button>
            </form>
            <p id="decryptResult"></p>
        </div>
        
        <script>
            function submitForm() {
                var xhr = new XMLHttpRequest();
                var form = document.getElementById("decryptForm");
                var url = form.action;
                var formData = new FormData(form);
                
                xhr.open("POST", url, true);
                xhr.onreadystatechange = function () {
                    if (xhr.readyState === 4 && xhr.status === 200) {
                        var response = JSON.parse(xhr.responseText);
                        document.getElementById("decryptResult").innerHTML = "Decrypted Message: " + response.result;
                    }
                };
                xhr.send(formData);
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html_form)

# Define the route for decryption


@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    cipher = request.form['cipher']
    key = request.form['key']
    decrypted_message = decrypt(cipher, key)
    return jsonify({'result': decrypted_message})


# Run the Flask app
if __name__ == '__main__':
    public_url = ngrok.connect(5000)
    print(f" * ngrok tunnel: {public_url}")
    app.run(port=5000)
