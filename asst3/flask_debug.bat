python -c "import os, subprocess; os.environ['FLASK_APP']='asst/__init__.py'; os.environ['FLASK_DEBUG']='1'; subprocess.Popen('python -m flask run --host=0.0.0.0', shell=True).wait()"
