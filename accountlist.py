#!/bin/python

import os
import re
import sqlite3

from swift.cli.info import print_info, InfoSystemExit
from swift.account.backend import AccountBroker

class AccountList:


    def __init__(self):
        self.device = '/srv/node'


    def findAccDir(self):
        acc_dir = []
        for dir_parent in os.listdir(self.device):
            for dir_child in os.listdir(self.device + '/' + dir_parent):
                if dir_child == 'accounts':
                    acc_dir.append(self.device + '/' + dir_parent + '/' + dir_child)
        return acc_dir


    def retreive_dir(self, file_or_dir):
        list_dir = []
        list_dir.append(file_or_dir)
        if not os.path.isdir(file_or_dir):
            return list_dir

        for x in os.listdir(file_or_dir):
            for cur in self.retreive_dir(file_or_dir + '/' + x):
                list_dir.append(cur)
        return list_dir

    def get_accountDB_path(self, file_or_dir):
        db_list = []
        for x in file_or_dir:
            if re.match('.*\.db$', x):
                db_list.append(x)
        return db_list


    def main(self):
        dir_list =  self.findAccDir()
        for _list in dir_list:
            for x in os.listdir(_list):
                y = self.retreive_dir(_list + '/' + x)
                db_files = self.get_accountDB_path(y)

                for db_file in db_files:
                    try:
                        info = AccountBroker(db_file).get_info()
                        print '%s %s' % (db_file, info)
                    except sqlite3.OperationalError as err:
                        if 'no such table' in str(err):
                            print "Does not appear to be a DB of type \"%s\": %s" % (
                                db_type, db_file)
                            raise InfoSystemExit()
                        raise                        


if __name__ == '__main__':
    accountList = AccountList()
    accountList.main()
