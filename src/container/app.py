from flask import Flask, request, render_template, jsonify
from server_form import RegistrationForm


from format_ini import create_ini
from game_manager import currently_running, start_new_instance 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def create_server():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        if len(currently_running()) == 0:
            config_id = create_ini(request.form)
            start_new_instance(config_id)
        else:
            return jsonify({'error': 'Not enough capacity'}), 405
    return render_template('register.html', form=form)
