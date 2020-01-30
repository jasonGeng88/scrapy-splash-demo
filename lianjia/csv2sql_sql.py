# -*- coding: utf-8 -*-

create_tbl_sql = '''
CREATE TABLE `lianjia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `location` varchar(50) NOT NULL DEFAULT '' COMMENT '板块，如春申、莘庄',
  `area_name` varchar(50) NOT NULL DEFAULT '' COMMENT '小区名称',
  `house_type` varchar(50) NOT NULL DEFAULT '' COMMENT '房屋类型',
  `size` double NOT NULL DEFAULT '0' COMMENT '面积大小',
  `link` varchar(50) NOT NULL DEFAULT '' COMMENT '链接',
  `transaction_time` date NOT NULL COMMENT '成交时间',
  `sticker_price` double NOT NULL DEFAULT '0' COMMENT '挂牌价',
  `transaction_price` double NOT NULL DEFAULT '0' COMMENT '成交价',
  `duration` int(11) NOT NULL DEFAULT '0' COMMENT '成交周期',
  `unit_price` double NOT NULL DEFAULT '0' COMMENT '单价',
  `floor_type` varchar(50) NOT NULL DEFAULT '' COMMENT '楼层',
  `building_year` int(11) NOT NULL DEFAULT '0' COMMENT '建造年份',
  `house_direction` varchar(50) NOT NULL DEFAULT '' COMMENT '房屋朝向',
  `fitment_type` varchar(50) NOT NULL DEFAULT '' COMMENT '装修类型',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1263 DEFAULT CHARSET=utf8;
'''

sql_format = '''insert into lianjia(
    `location`,
    `area_name`,
    `house_type`,
    `size`,
    `link`,
    `transaction_time`,
    `sticker_price`,
    `transaction_price`,
    `duration`,
    `unit_price`,
    `floor_type`,
    `building_year`,
    `house_direction`,
    `fitment_type`
    ) values %s
'''


def main():
    filenames = [
        "lianjia_chunshen_202001302041.csv",
        "lianjia_jinganxincheng_202001302038.csv",
        "lianjia_qibao_202001302016.csv",
        "lianjia_xinzhuang5_202001302045.csv"
    ]
    items = []
    for filename in filenames:
        filename_arr = filename.split("_")
        location = filename_arr[1]
        f = open(filename, "r")
        for line in f:
            # 黎明花园,1室1厅,52.24平米,https://sh.lianjia.com/chengjiao/107101427144.html,2020.01.11,232,挂牌244万,成交周期212天,44411,低楼层(共6层),1997年建板楼,南 , 简装
            # "黎明花园","1室1厅","52.24","https://sh.lianjia.com/chengjiao/107101427144.html","2020-01-11","244","232","212","44411","低楼层(共6层)","1997","南","简装"
            arr = line.split(",")
            area_name = arr[0].strip()
            house_type = arr[1].strip()
            size = arr[2].replace("平米", "").strip()
            link = arr[3].strip()
            transaction_time = arr[4].replace(".", "-").strip()
            sticker_price = arr[6].replace("挂牌", "").replace("万", "").strip()
            transaction_price = arr[5].strip()
            duration = arr[7].replace("成交周期", "").replace("天", "").strip()
            unit_price = arr[8].strip()
            floor_type = arr[9].strip()
            building_year = arr[10][0:4]
            if len(building_year) < 4:
                building_year = 0

            house_direction = arr[11].strip()
            fitment_type = arr[12].strip()

            item = "(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")" % (location, area_name, house_type, size, link, transaction_time, sticker_price, transaction_price, duration, unit_price, floor_type, building_year, house_direction, fitment_type)
            items.append(item)
        f.close()

    sql = sql_format % (",".join(items))

    wf = open("insert.sql", "w")
    wf.write(sql)
    wf.close()
    pass


if __name__ == '__main__':
    main()
