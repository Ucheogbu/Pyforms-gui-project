import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText
from pyforms.controls import ControlButton
from pyforms.controls import ControlLabel
from pyforms.controls import ControlList
from datetime import datetime as dt
import time
# import json


class Filter(BaseWidget):
    def __init__(self):
        super().__init__('Site Filter')

        # Make Ui Components

        self._toggle_label = ControlLabel('Click The Button If You Want to Change Your Host Path')
        self.start_help = ControlLabel('Type in the hour of the day you want the filter to start working. '
                                       '\n we are using a 24 hour clock EG if you want it'
                                       ' to start working by 5am \ntype 5 but if you want 5pm type 17\n'
                                       'default this is set to 9am ''or 9 O\'clock in the morning.\n'
                                       ' Please type only digits no letters '
                                       '\nor press Submit to use ''default time of 9am: ')
        self.stop_help = ControlLabel('Type in the hour of the day you want the filter to stop working. '
                                      '\n we are using a 24 hour clock EG if you want it'
                                      ' to stop working by 5am \ntype 5 but if you want 5pm type 17\n'
                                      'default this is set to 5pm ''or 5 O\'clock in the evening.\n'
                                      ' Please type only digits no letters '
                                      '\nor press Submit to use ''default time of 5pm: ')
        self._set_path_button = ControlButton('Toggle Host Path Form', checkable=True)
        self._set_host_path = ControlText('Set Host Path', enabled=False)
        self._host_submit_button = ControlButton('Submit', enabled=False)
        self._result_label = ControlLabel('')
        self._start_button = ControlButton('Start')
        self._stop_button = ControlButton('Stop')
        self._get_site_field = ControlText('Enter Sites You wish to Block')
        self._next_button = ControlButton('Next')
        self._done_button = ControlButton('Done')
        self._start_submit_button = ControlButton('Submit')
        self._stop_submit_button = ControlButton('Submit')
        self.raw_stop = ControlText('Please enter Stop time', width=50)
        self.raw_start = ControlText('Please Enter Start time', width=50)
        self._siteList = ControlList('Sites', remove_function=self.__rm_person_btn_action)
        self._block_history = ControlList('History')
        self._block_history.horizontal_headers = ['Blocked Sites', 'TIme']
        self._siteList.horizontal_headers = ['Blocked Sites']

        # Assign Buttons to handlers(Functions)

        self._set_path_button.value = self.toggle_host_box
        self._host_submit_button.value = self.submit_host_path
        self._next_button.value = self.get_next_site
        self._start_submit_button.value = self.set_start_time
        self._stop_submit_button.value = self.set_stop_time
        self._done_button.value = self.finish

        # Assign Global Variables/Properties

        self.redirect = '127.0.0.1'
        self.check = self.check_time()
        self.start = 9
        self.stop = 17
        self.sites = []
        self.host_path_temp = ''
        self.host_path = ''
        self.sites_that_kill_me = []

        # Arrange Gui using the formset property

        self._formset = [
            {
                'a:Add Site': [('_toggle_label', '_set_path_button'), ('_set_host_path', '_host_submit_button'),
                               ('raw_start', '_start_submit_button'),
                               ('raw_stop', '_stop_submit_button'),
                               ('_get_site_field', '_next_button', '_done_button'), ('_start_button', '_stop_button'),
                               '_result_label'],
                'b:Site List': ['_siteList'],
                'c:Block History':['_block_history'],
                'd:Help':['start_help', '=', 'stop_help']
            }
        ]

        # This Toggle the change host path form so user can be able to change host path

    def toggle_host_box(self):
        if self._set_host_path.enabled is False:
            self._set_host_path.enabled = True
            self._host_submit_button.enabled = True
        else:
            self._set_host_path.enabled = False
            self._host_submit_button.enabled = False

        # This function moves the value(i.e the site to be blocked from the form to the store and returns the form

    def get_next_site(self):
        if self._get_site_field.value != '':
            self.sites.append(self._get_site_field.value)
        else:
            pass
        self._get_site_field.value = ''

        # This function moves the value(i.e the site to be blocked) from the store to the siteList
        # and the blocked history tab tab and calls the process form function

    def finish(self):
        self._get_site_field.enabled = False
        for site in self.sites:
            if site not in self._siteList:
                self._siteList += [str(site)]

        # for site in self.sites:
        #     if site not in self._block_history:
        #         block_time = dt.now()
        #         self._block_history += [str(site), str(block_time)]
        # self.process_sites()

    def submit_host_path(self):
        self.host_path = self._set_host_path.value
        self._set_host_path.enabled = False

    def __rm_person_btn_action(self):
        index = self._siteList.selected_row_index
        self._siteList -= index
        pass

    def get_host_paths(self):
        default_host_path = r"C:\Windows\System32\drivers\etc\hosts"

        if self.host_path == '':
            self.host_path = default_host_path
        else:
            self.host_path = r"%s" % self.host_path
        return self.host_path

    def process_sites(self):
        while 1:
            if len(self.sites) == 0:
                try:
                    raise IOError
                except IOError:
                    self.warning_popup('Please enter at least one website', buttons='Ok')
            else:
                for wsite in self.sites:
                    if 'www.' not in wsite:
                        site = r"www." + r"%s" % wsite
                        self.sites_that_kill_me.append(site)
                        self.sites_that_kill_me.append(wsite)
                break

    def set_start_time(self):
        count = 0
        if self.raw_start == '':
            self.raw_start = 9
            self.start = self.raw_start

        elif self.raw_start in range(0, 25):
            self.start = self.raw_start

        else:
            self.warning_popup('Please type a number between 1 and 24')
            count += 1
            if count == 5:
                print(self.start_help)
        return self.start

    def set_stop_time(self):
        count = 0
        while 1:

            if self.raw_stop == 9:

                self.stop = self.raw_stop
                break
            elif self.raw_stop in range(0, 25):
                self.stop = self.raw_stop
                break
            else:
                print('Please type a number between 1 and 24')
                count += 1
                if count == 5:
                    print(self.stop_help)
                    count = 0
        return self.stop

    def check_time(self):

        if dt(dt.now().year, dt.now().month, dt.now().day, self.start) < dt.now() < dt(dt.now().year, dt.now().month,
                                                                                       dt.now().day, self.stop):
            return True
        else:
            return False

    def modify_host(self):
        if self.check is True:
            print('Working Time!!')
            with open(self.host_path, 'r+') as file:
                content = file.read()
                for site in self.sites_that_kill_me:
                    if site in content:
                        pass
                    else:
                        file.write(self.redirect + ' ' + site + '\n')
            time.sleep(60000)
        else:
            with open(self.host_path, 'r+') as file:
                content = file.readlines()
                file.seek(0)
                for line in content:
                    if not any(site in line for site in self.sites_that_kill_me):
                        file.write(line)
                file.truncate()
            print('Time to play')
            time.sleep(60000)

    # def main():
    #     sites = input('type the url of the sites you wish to block separated by commas')
    #     host_path = input('Type in the path of your hosts file if you are not on a windows system \n or'
    #                       ' if you changed the location ELSE press enter: ')
    #     redirect = '127.0.0.1'
    #     hosts_path = get_host_paths(host_path)
    #     site_that_kill_me = get_sites(sites)
    #     start = set_start_time()
    #     stop = set_stop_time()
    #     check = check_time(start, stop)
    #     while 1:
    #         modify_host(hosts_path, site_that_kill_me, redirect, check)
    #
    # if __name__ == '__main__':
    #     main()


if __name__ == '__main__':
    pyforms.start_app(Filter)
