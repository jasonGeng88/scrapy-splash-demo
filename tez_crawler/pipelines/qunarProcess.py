# -*- coding: utf-8 -*-
import logging
import datetime


def insert(tx, item):
    logging.info('############[QunarProcess info]############')
    print item
    sql = '''INSERT INTO qunar (
                            `price`,
                            `go_flight_code`,
                            `back_flight_code`,
                            `go_dep_time`,
                            `go_arr_time`,
                            `back_dep_time`,
                            `back_arr_time`,
                            `start_time`,
                            `end_time`,
                            `create_time`
                          )
            VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}")
            ON DUPLICATE KEY UPDATE
            `price` = "{0}",
            `go_flight_code` = "{1}",
            `back_flight_code` = "{2}",
            `go_dep_time` = "{3}",
            `go_arr_time` = "{4}",
            `back_dep_time` = "{5}",
            `back_arr_time` = "{6}",
            `start_time` = "{7}",
            `end_time` = "{8}"
            '''

    sql = sql.format(item['price'][0],
                     item['go_flight_code'][0],
                     item['back_flight_code'][0],
                     item['go_dep_time'][0],
                     item['go_arr_time'][0],
                     item['back_dep_time'][0],
                     item['back_arr_time'][0],
                     item['start_time'][0],
                     item['end_time'][0],
                     datetime.datetime.now()
                     )
    try:
        tx.execute(sql)
    except Exception, e:
        logging.error(e)
        logging.error(sql)
