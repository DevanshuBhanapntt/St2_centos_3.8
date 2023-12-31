#!/usr/bin/env python
# Copyright 2021 NTT Data
# Developed by Nalinikant11.Mohanty@nttdata.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# from st2common.runners.base_action import Action

import datetime
import os
import sys
import ast
from st2client.client import Client
from lib.base_action import BaseAction

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../actions/lib')


class GetTopCIIncidentDetails(BaseAction):
    def __init__(self, config):
        """Creates a new Action given a StackStorm config object (kwargs works too)
        :param config: StackStorm configuration object for the pack
        :returns: a new Action
        """
        super(GetTopCIIncidentDetails, self).__init__(config)

    def get_inc(self, inc_data, daily_data, weekly_data, monthly_data, config_item, customer):
        today = str(datetime.datetime.today().date())
        lastday = str(datetime.datetime.today().date() - datetime.timedelta(days=30))
        # update the company name in the notes , according to the account.
        notes = "\n\nThis Problem ticket was generated by automation and assigned to the Problem Owner identified for the "+customer+" account to further investigate the high ticket trend and to perform the RCA."
        notes += "\n\nTicket Count Thresholds for "+customer+"\n30 Days - 15 Tickets\n7 Days - 10 Tickets\n1 Day - 5 Tickets"
        notes += "\n\nDate Range - {} to {}\n".format(lastday, today)
        notes += "\n\nConfigured Item Name : {}\nTicket Total for 30 Days = {}\nTicket Total for 7 Days = {}\nTicket Total for 1 Day = {}\n\n\n\nTicket Details:".format(config_item,monthly_data,weekly_data,daily_data)

        try:
            inc_lst = inc_data.split("$")
            for inc_rec in inc_lst:
                res = ast.literal_eval(inc_rec)
                notes = notes + "\nTicket Type: " + str(res['DemandSignalType']) + "\nTicket ID: " + str(res['DemandSignalID']) + "\nTicket Details: " + str(res['Activity']) + "\n"

            result = (True, {"notes": notes})
        except Exception as e:
            print(e)
            result = (False, {"notes": notes})

        return result

    def run(self, inc_data, daily_data, weekly_data, monthly_data, config_item, customer):
        return_value = self.get_inc(inc_data, daily_data, weekly_data, monthly_data, config_item, customer)
        return return_value
