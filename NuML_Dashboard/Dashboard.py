from flask import Flask, flash, render_template, Response, request, redirect, url_for
from werkzeug.utils import secure_filename
import subprocess
import os
import winreg

UPLOAD_FOLDER = '..\\models_upload'
NN_PROJ_FOLDER = '..\\nn_project'
NuML_TFLM_Tool = '..\\NuML_TFLM_Tool'

ALLOWED_EXTENSIONS = set(['tflite'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.secret_key = "secret key" 

application_info = {
    'generic': 'Generic',
    'imgclass': 'Image Classification',
    'objdet': 'Object Detection'
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(NN_PROJ_FOLDER, exist_ok=True)

_upload_tfile_file = None
_uv4_dir = 'C:\\Keil_v5\\UV4'
_application = 'generic'
_custom_arena_enble = False
_arena_size = 512000

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def read_registry_value(hive, subkey, value_name):
    """
    Reads a value from the Windows Registry.

    Args:
        hive: The root key of the registry (e.g., winreg.HKEY_LOCAL_MACHINE).
        subkey: The path to the subkey (e.g., "SOFTWARE\\Microsoft\\Windows\\CurrentVersion").
        value_name: The name of the value to read (e.g., "ProgramFilesDir").

    Returns:
        The data of the specified value, or None if an error occurs.
    """
    try:
        # Open the specified registry key
        key_handle = winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ)

        # Query the value data
        value_data, value_type = winreg.QueryValueEx(key_handle, value_name)

        # Close the key handle
        winreg.CloseKey(key_handle)

        return value_data

    except FileNotFoundError:
        print(f"Error: Registry key '{subkey}' or value '{value_name}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@app.route("/")
def index():
    if _uv4_dir != None:
        flash(f'--ide_tool: {_uv4_dir}\\UV4.exe')

    if _application != None:
        flash(f'--application: {_application}')

    if _custom_arena_enble == True:
        flash(f'--model_arena_size: {_arena_size}')

    if _upload_tfile_file != None:
        flash(f'--model_file: {os.path.basename(_upload_tfile_file)}')
        disable_gen = ""
    else:
        flash(f'Please upload tflite file')
        disable_gen = "disabled"
    return render_template('index.html', uv4_dir_path = _uv4_dir, generate_disable = disable_gen, app_info = application_info, app_sel = _application, enable_custom_arena = _custom_arena_enble, arena_size = _arena_size)

@app.route('/stream')
def stream():
    def generate():
        if _upload_tfile_file == None:
            yield "data: finished\n\n"
            return Response(generate(), mimetype='text/event-stream')

        print(_upload_tfile_file)
        cur_dir = os.getcwd()
        os.chdir(NuML_TFLM_Tool)
        print(os.getcwd())
        uv4_path = os.path.join(_uv4_dir, 'UV4.exe')
        proj_deploy_cmd = ["python", "numl_tool.py", "deploy", "--board", "NuMaker-M55M1", "--project_type", "uvision5_armc6", "--ide_tool", uv4_path, "--output_path", NN_PROJ_FOLDER, "--model_file", _upload_tfile_file, "--application" , _application]

        if _custom_arena_enble == True:
            proj_deploy_cmd.extend(['--model_arena_size', _arena_size])

        process = subprocess.Popen(
            proj_deploy_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in process.stdout:
            yield f"data: {line}\n\n"

        for line in process.stderr:
            yield f"data: {line}\n\n"

        yield "data: finished\n\n"
        os.chdir(cur_dir)
        print(os.getcwd())
    return Response(generate(), mimetype='text/event-stream')

@app.route('/UV4', methods=['POST'])
def UV4():
    file_path = request.form['uv4_dir']
    global _uv4_dir
    _uv4_dir = file_path
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        global _upload_tfile_file
        _upload_tfile_file = os.path.join(app.config['UPLOAD_FOLDER'], filename) 
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        flash('Allowed file types is tflite')
    return redirect(url_for('index'))

@app.route('/application', methods=['POST'])
def application():
    global _application
    _application = request.form['application']
    return redirect(url_for('index'))

@app.route('/arena', methods=['POST'])
def arena():
    global _custom_arena_enble
    if request.form.get('enable_arena'):
        _custom_arena_enble = True
        global _arena_size
        _arena_size = request.form.get('arena_size')
    else:
        _custom_arena_enble = False

    return redirect(url_for('index'))

if __name__ == '__main__':

    if os.name == 'nt':
        hive = winreg.HKEY_LOCAL_MACHINE
        subkey = "SOFTWARE\\WOW6432Node\\Keil\\Products\\MDK"
        value_name = "Path"
        Keil_path = read_registry_value(hive, subkey, value_name)

        if Keil_path != None:
            _uv4_dir = os.path.dirname(Keil_path)
            _uv4_dir = os.path.join(_uv4_dir, 'UV4')

    app.run()