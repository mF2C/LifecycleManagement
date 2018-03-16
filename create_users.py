
import requests
from usermgnt.utils.logs import LOG


# create_user: create a user in cimi
def create_admin_user():
    try:
        body = {
                "userTemplate": {
                    "href": "user-template/auto",
                    "password": "E9E633097AB9CEB3E48EC3F70EE2BEBA41D05D5420EFEE5DA85F97D97005727587FDA33EF4FF2322088F4C79E8133CC9CD9F3512F4D3A303CBDB5BC585415A00",
                    "emailAddress": "mf2c-developers@lists.atosresearch.eu",
                    "roles": "ADMIN",
                    "username": "testuser",
                    "firstName": "Test",
                    "state": "ACTIVE",
                    "organization": "mF2C",
                    "lastName": "User",
                    "resourceURI": "http://sixsq.com/slipstream/1/User",
                    "isSuperUser": False
                }
            }

        r = requests.post('https://localhost/api/user',
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
        LOG.error('Exception')


def create_anon_user():
    try:
        body = {
                "userTemplate": {
                    "href": "user-template/auto",
                    "password": "E9E633097AB9CEB3E48EC3F70EE2BEBA41D05D5420EFEE5DA85F97D97005727587FDA33EF4FF2322088F4C79E8133CC9CD9F3512F4D3A303CBDB5BC585415A00",
                    "emailAddress": "mf2c-developers2@lists.atosresearch.eu",
                    "roles": "ANON",
                    "username": "testuser2",
                    "firstName": "Test2",
                    "state": "ACTIVE",
                    "organization": "mF2C",
                    "lastName": "User",
                    "resourceURI": "http://sixsq.com/slipstream/1/User",
                    "isSuperUser": False
                }
            }

        r = requests.post('https://localhost/api/user',
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
        LOG.error('Exception')


###############################################################################

def main():
    # '''
    # create users
    LOG.info("-------------------------------")
    create_admin_user() # testuser
    create_anon_user()  # testuser2
    LOG.info("-------------------------------")
    # '''


if __name__ == "__main__":
    main()


