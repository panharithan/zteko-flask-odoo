#!/bin/env python
import sys
import os
sys.path.insert(1,os.path.abspath("./pyzk"))
from zk import ZK, const
from odoo_rpc_client import Client
from datetime import datetime

#!/bin/env python
import sys
import os
sys.path.insert(1,os.path.abspath("./pyzk"))
from zk import ZK, const
from datetime import datetime
import xmlrpc.client


def get_user_name(all_users, user_id):
    for user in all_users:
        if user.get('id', False) == user_id:
            return user.get('name')
    return 'Unknown'


def send_data_to_erp(name, timestamp, punch, url, db, email, password):
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    user = common.authenticate(db, email, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    rpc_request = models.execute_kw(
        db, user, password,
        'hr.attendance', 'rpc_generate_attendance', [[]],
        {'employee_name': name,
         'timestamp': timestamp,
         'punch': punch,
        })


def excecute_pyzk(finger_print_ip='192.168.1.201', target_date=None, odoo_ip=None, odoo_db=None, odoo_email=None, odoo_password=None):
    conn = None
    # create ZK instance
    zk = ZK(finger_print_ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
    try:
        # connect to device
        conn = zk.connect()
        # disable device, this method ensures no activity on the device while the process is run
        conn.disable_device()

        # get all current users
        user_names = [{"id": str(user.uid), "name": user.name} for user in conn.get_users()]

        # calculate target date
        if not target_date:
            target_date = datetime.today().strftime("%Y-%m-%d")

        attendances = conn.get_attendance()
        for attend in attendances:
            if format(attend.timestamp.strftime("%Y-%m-%d")) == target_date:
                send_data_to_erp(
                    get_user_name(user_names, attend.user_id),
                    attend.timestamp,
                    attend.punch,
                    str('http://' + odoo_ip + ':8069'),
                    odoo_db,
                    odoo_email,
                    odoo_password
                )

        # Test Voice: Say Thank You
        conn.enable_device()
    except Exception as e:
        print("Process terminate : {}".format(e))
    finally:
        if conn:
            conn.disconnect()
