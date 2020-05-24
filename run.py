from flask import Flask, render_template
from forms import QueryForm
from flask_bootstrap import Bootstrap
from tool import excecute_pyzk

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc"

bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = QueryForm()
    if form.validate_on_submit():
        odoo_ip = form.odoo_ip.data
        finger_print_ip = form.finger_print_ip.data
        odoo_db = form.odoo_db_name.data
        odoo_email = form.odoo_email.data
        odoo_password = form.odoo_password.data
        entry_date = form.entry_date.data
        target_date = entry_date.strftime("%Y-%m-%d")

        try:
            excecute_pyzk(
                finger_print_ip=finger_print_ip,
                target_date=target_date,
                odoo_ip=odoo_ip,
                odoo_db=odoo_db,
                odoo_email=odoo_email,
                odoo_password=odoo_password,
            )
        except:
            raise("Something went wrong")

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(port=5550)
