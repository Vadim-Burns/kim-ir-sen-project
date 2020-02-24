from flask import Flask
import os
import db
from flask import request, abort, render_template
from cryptography.fernet import Fernet

app = Flask(__name__, static_folder=os.path.join(os.getcwd() + "/static"))
security_key = os.environ.get("SECURITY_KEY")
main_fernet = Fernet(security_key.encode())


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        return app.send_static_file('create.html')
    else:
        text = request.form.get("text")
        if text is None:
            return abort(400)

        key = Fernet.generate_key()
        f = Fernet(key)
        encrypted_text = f.encrypt(text.encode())
        id = db.Note.create(text=encrypted_text.decode()).id

        super_key = main_fernet.encrypt((str(id) + "=" + key.decode()).encode()).decode()
        return render_template('code.html', code=super_key)


@app.route("/find", methods=['POST'])
def find():
    super_key = request.form.get("key")
    if super_key is None:
        return 400

    super_key_decrypted = main_fernet.decrypt(super_key.encode()).decode()

    index = super_key_decrypted.find("=")
    id = int(super_key_decrypted[:index])
    key = super_key_decrypted[index + 1:]

    encrypted_text = db.Note.get_text_by_id(id)
    if encrypted_text is None:
        return abort(404)

    f = Fernet(key)
    text = f.decrypt(encrypted_text.encode()).decode()

    return render_template("note.html", text=text)


@app.route('/api/add', methods=["POST"])
def add():
    """
    This function checks if json_data is valid, then generate random key and save
    encrypted text to database. Then generates access code for user note.id + "=" + key for text.
    """
    json_data = request.get_json()
    if json_data is None or json_data.get("text") is None:
        abort(400)

    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted_text = f.encrypt(json_data.get("text").encode())
    id = db.Note.create(text=encrypted_text.decode()).id

    super_key = main_fernet.encrypt((str(id) + "=" + key.decode()).encode()).decode()
    return {"key": super_key}


@app.route('/api/get', methods=["POST"])
def get():
    """
    This function checks if json_data is valid, then decrypt user access code and get id of Note.
    After that it decrypts text from note and sends back to user.
    """
    json_data = request.get_json()
    if json_data is None or json_data.get("key") is None:
        abort(400)

    try:
        super_key_decrypted = main_fernet.decrypt(json_data.get("key").encode()).decode()

        index = super_key_decrypted.find("=")
        id = int(super_key_decrypted[:index])
        key = super_key_decrypted[index + 1:]

        encrypted_text = db.Note.get_text_by_id(id)
        if encrypted_text is None:
            return abort(404)

        f = Fernet(key)
        text = f.decrypt(encrypted_text.encode()).decode()

        return {"text": text}
    except:
        return {"error": "Wrong key"}, 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
