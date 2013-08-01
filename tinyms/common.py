__author__ = 'tinyms'

import os, sys, re
import hashlib, json
import urllib.request
import urllib.parse

import psycopg2
import psycopg2.extras


class Postgres():
    DATABASE_NAME = ""
    USER_NAME = ""
    PASSWORD = ""

    @staticmethod
    #Connect to Postgres Database
    def open():
        return psycopg2.connect(database=Postgres.DATABASE_NAME,
                                user=Postgres.USER_NAME,
                                password=Postgres.PASSWORD)

    @staticmethod
    def update(sql, params, return_col_name = None):

        """
        for Insert,Update,Delete
        :param sql:
        :param params:
        :param return_col_name: last insert row id etc.
        :return:
        """
        if return_col_name:
            sql += " RETURNING %s" % return_col_name
        cnn = None
        try:
            cnn = Postgres.open()
            cur = cnn.cursor()
            cur.execute(sql, params)
            if return_col_name:
                result = cur.fetchone()[0]
            else:
                result = True
            cnn.commit()
        except psycopg2.DatabaseError as e:
            print("Error %s" % e)
            cnn.rollback()
            result = False
        finally:
            if cnn:
                cnn.close()

        return result

    @staticmethod
    #Batch Insert,Update,Delete
    def update_many(sql, arr_params):
        try:
            cnn = Postgres.open()
            cur = cnn.cursor()
            cur.executemany(sql, arr_params)
            cnn.commit()
        except psycopg2.DatabaseError as e:
            print("Error %s" % e)
        finally:
            if cnn:
                cnn.close()

    @staticmethod
    #Query DataSet
    def many(sql, params, callback=None):
        dataset = list()
        cnn = None
        try:
            cnn = Postgres.open()
            cur = cnn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(sql, params)
            rows = cur.fetchall()
            for row in rows:
                c = row.copy()
                if callback:
                    callback(c)
                dataset.append(c)
            cur.close()
        except psycopg2.DatabaseError as e:
            print("Error %s" % e)
        finally:
            if cnn:
                cnn.close()
        return dataset

    @staticmethod
    #First Row Data
    def row(sql, params, callback=None):
        items = Postgres.many(sql, params, callback)
        if len(items) > 0:
            return items[0]
        return None

    @staticmethod
    #First Column Data
    def col(sql, params, callback=None):
        items = Postgres.many(sql, params, callback)
        cols = list()
        for item in items:
            values = [i for i in item.values()]
            if len(values) > 0:
                cols.append(values[0])
        return cols

    @staticmethod
    #First Row And First Column
    def one(sql, params, callback=None):
        first_col = Postgres.col(sql, params, callback)
        if len(first_col) > 0:
            return first_col[0]
        return None

    @staticmethod
    #Store Proc, Return Single Result
    def proc_one(name, params, callback=None):
        first_col = Postgres.proc_many(name, params, callback)
        if len(first_col) > 0:
            return first_col[0]
        return None

    @staticmethod
    #Store Proc, Return DataSet
    def proc_many(name, params, callback=None):
        dataset = list()
        cnn = None
        try:
            cnn = Postgres.open()
            cur = cnn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            rows = cur.callproc(name, params)
            for row in rows:
                c = row.copy()
                if callback:
                    callback(c)
                dataset.append(c)
            cur.close()
        except psycopg2.DatabaseError as e:
            print("Error %s" % e)
        finally:
            if cnn:
                cnn.close()
        return dataset

    @staticmethod
    #Return all cols name from current Query cursor
    def col_names(cur):
        names = list()
        for col in cur.description:
            names.append(col.name)
        return names

class Utils():
    @staticmethod
    def text_read(file_nme):
        f = open(file_nme)
        all = f.readlines()
        f.close()
        return all

    @staticmethod
    def text_write(f_name, lines=[], suffix="\n"):
        f = open(f_name, "w+")
        for line in lines:
            f.write(line + suffix)
        f.close()

    @staticmethod
    def url_with_params(url):
        r1 = urllib.parse.urlsplit(url)
        if r1.query != "":
            return True
        return False

    @staticmethod
    def trim(text):
        return "".join(text.split())

    @staticmethod
    def md5(s):
        h = hashlib.new('ripemd160')
        h.update(bytearray(s.encode("utf8")))
        return h.hexdigest()

    @staticmethod
    def mkdirs(path):
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True
        else:
            return False

    @staticmethod
    def parse_int(text):
        nums = Utils.parse_int_array(text)
        if len(nums) > 0:
            return int(nums[0])
        return None

    @staticmethod
    def parse_int_array(text):
        arr = list()
        p = re.compile("\\d+", re.M)
        nums = p.findall(text)
        if len(nums) > 0:
            arr = [int(s) for s in nums]
        return arr

    @staticmethod
    def parse_date_text(text):
        p = re.compile("\\d{4}-\\d{2}-\\d{2}")
        dates = p.findall(text)
        if len(dates) > 0:
            return dates[0]
        return ""

    @staticmethod
    def parse_datetime_text(text):
        p = "\\d{2}-\\d{2}\\s{1}\\d{2}:\\d{2}"
        r = re.compile(p)
        matchs = r.findall(text)
        if len(matchs) > 0:
            return matchs[0]
        return ""

    @staticmethod
    def parse_float(text):
        floats = Utils.parse_float_array(text)
        if len(floats) > 0:
            return float(floats[0])
        return None

    @staticmethod
    def parse_float_array(text):
        p = re.compile("\\d+\\.\\d+", re.M)
        return [float(s) for s in p.findall(text)]

    @staticmethod
    def encode(obj):
        return json.dumps(obj)

    @staticmethod
    def decode(text):
        return json.loads(text)

    @staticmethod
    def download(url, save_path):
        try:
            f = urllib.request.urlopen(url, timeout=15)
            data = f.read()
            with open(save_path, "wb") as cache:
                cache.write(data)
        except urllib.error.URLError as ex:
            info = sys.exc_info()
            print(info[0], ":", info[1], ex)

    @staticmethod
    def matrix_reverse(arr):
        return [[r[col] for r in arr] for col in range(len(arr[0]))]

