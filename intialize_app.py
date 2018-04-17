
import requests
import sys, traceback
from lifecycle import config
from lifecycle.utils.logs import LOG
from slipstream.api import Api


# ACL
acl = {"owner":
           {"principal": config.dic['CIMI_USER'],
            "type": "ROLE"},
       "rules": [{"principal": config.dic['CIMI_USER'],
                  "type": "ROLE",
                  "right": "ALL"},
                 {"principal": "ANON",
                  "type": "ROLE",
                  "right": "ALL"}
                 ]}


# create_user: create a user in cimi
def create_user_1():
    try:
        body = {
                "userTemplate": {
                    "href": "user-template/self-registration",
                    #"roles": "ADMIN",
                    "password": "password",
                    "passwordRepeat" : "password",
                    "emailAddress": "rsucasas@gmail.com",
                    "username": "rsucasas"
                }
            }

        r = requests.post('https://dashboard.mf2c-project.eu/api/user',
                          verify=False,
                          headers={'Content-Type': 'application/json',
                                  'Accept': 'application/json'},
                          json=body)
        LOG.debug(str(r))
        LOG.debug(r.content)
        LOG.debug(r.status_code)
        LOG.debug(r.ok)
        if r.status_code == 201:
            LOG.info('OK')
        else:
            LOG.error('ERROR')
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')


def create_anon_user():
    try:
        body = {
                "userTemplate": {
                    "href": "user-template/self-registration",
                    #"roles": "ADMIN",
                    "password": "testpassword",
                    "passwordRepeat" : "testpassword",
                    "emailAddress": "testuser@gmail.com",
                    "username": "rsucasas2"
                }
            }

        r = requests.post('https://192.168.252.41/api/user',
                          verify=False,
                          headers={'Content-Type': 'application/json',
                                  'Accept': 'application/json'},
                          json=body)
        LOG.debug(str(r))
        LOG.debug(r.content)
        LOG.debug(r.status_code)
        LOG.debug(r.ok)
        if r.status_code == 201:
            LOG.info('OK')
        else:
            LOG.error('ERROR')
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')


def add_service_1():
    try:
        api = Api(config.dic['CIMI_URL'],
                  insecure=True,
                  cookie_file=config.dic['CIMI_COOKIES_PATH'],
                  login_creds={'username': config.dic['CIMI_USER'],
                               'password': config.dic['CIMI_PASSWORD']})

        # test api
        resp = api.cimi_search('users')
        LOG.info('connected to ' + config.dic['CIMI_URL'] + ": total users: " + str(resp.count))

        body = {
                "name": "EMS",
                "description": "Emergency Management System",
                "category": {
                    "cpu": "low",
                    "memory": "low",
                    "storage": "low",
                    "inclinometer": True,
                    "temperature": True,
                    "jammer": True,
                    "location": True
                }
            }

        api.cimi_add("services", body)

        resp = api.cimi_search('services')
        LOG.info('connected to ' + config.dic['CIMI_URL'] + ": total services: " + str(resp.count))

        '''
        r = requests.post('https://192.168.252.41/api/service',
                          verify=False,
                          headers={'Content-Type': 'application/json',
                                  'Accept': 'application/json'},
                          json=body)
        LOG.debug(str(r))
        LOG.debug(r.content)
        LOG.debug(r.status_code)
        LOG.debug(r.ok)
        
        if r.status_code == 201:
            LOG.info('OK')
        else:
            LOG.error('ERROR')
        '''
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')


###############################################################################

def main():
    # '''
    # create users
    LOG.info("-------------------------------")
    create_user_1()
    #add_service_1()
    LOG.info("-------------------------------")
    # '''


if __name__ == "__main__":
    main()


