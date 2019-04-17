
# Run with `xvfb-run python argon-service.py`
from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymongo
import time
import subprocess
from time import time as now
connection_list = list()



class Browser(object):
    def __init__(self):
        pass

    def kill_firefox(self):
        try:
            # Kill firefox
            p = subprocess.Popen(['pkill', 'firefox'],
                                 stdout=subprocess.PIPE)
            res, error = p.communicate()
        except Exception as e:
            print(e)

    def open_browser(self, dao):
        try:
            self.display = Display(visible=0, size=(1024, 768))
            self.display.start()
            self.driver = webdriver.Firefox()
            self.driver.get("https://mainnet.aragon.org/#/{}/".format(dao))
        except Exception as e:
            self.display.stop()
            self.driver = None


    def start(self, dao):
        self.kill_firefox()
        self.open_browser(dao)

        time.sleep(20)

        if self.driver == None:
            return 'Undifind'

        content = self.driver.find_elements_by_class_name('item')
        # self.driver.save_screenshot(str(now())+'.png') # check state
        for element in content:
            if element.text == 'Settings':
                element.click()
                lis = self.driver.find_elements_by_tag_name('li')
                for li in lis:
                    if 'FINANCE' in li.text:
                        t = li.text
                        self.display.stop()
                        return t.split('\n')[1]
        self.display.stop()
        return None


def create_connection():
    client = pymongo.MongoClient('mongodb://localhost:27017/', connect=False)
    connection_list.append(client)
    return client['blankdao']


def close_connections():
    for con in connection_list:
        con.close()


def get_dao_list():
    db = create_connection()
    return db.dao.find({'processed': False})


while True:
    dao_list = get_dao_list()
    db = create_connection()
    for dao in dao_list:
        print('Start {} DAO'.format(dao['dao']))
        browser = Browser()
        res = browser.start(dao['dao'])
        print('RESUALT: ', res)
        if res == 'Undifind':
            continue
        if res == None:
            db.dao.update_one({
                '_id': dao['_id']
            }, {'$set': {
                'counter': dao['counter'] + 1,
                'processed': True if dao['counter'] >= 5 else False
            }}, upsert=False)
            continue

        db.dao.update_one({
            '_id': dao['_id']
        }, {'$set': {
            'address': res,
            'confirm': True,
            'processed': True
        }}, upsert=False)
    close_connections()
    print('Wait for 10 second')
    time.sleep(10)
