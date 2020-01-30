-- 成交量走势
select DATE_FORMAT(transaction_time,'%Y-%m'), count(*) from lianjia where transaction_time >= '2015-01-01' group by DATE_FORMAT(transaction_time,'%Y-%m')
-- 成交价走势
select DATE_FORMAT(transaction_time,'%Y-%m'), ROUND(avg(unit_price/10000),2) from lianjia where transaction_time >= '2015-01-01' group by DATE_FORMAT(transaction_time,'%Y-%m')

-- 成交量走势(静安新城)
select DATE_FORMAT(transaction_time,'%Y-%m'), count(*) from lianjia where transaction_time >= '2015-01-01' and area_name like '静安新城%' group by DATE_FORMAT(transaction_time,'%Y-%m')
-- 成交价走势(静安新城)
select DATE_FORMAT(transaction_time,'%Y-%m'), ROUND(avg(unit_price/10000),2) from lianjia where transaction_time >= '2015-01-01'  and area_name like '静安新城%' group by DATE_FORMAT(transaction_time,'%Y-%m')

-- 成交量走势(静安新城-各区)
select area_name from lianjia where transaction_time >= '2015-01-01' and area_name like '静安新城%' group by area_name
--> 
-- 静安新城一区
-- 静安新城七区
-- 静安新城三区
-- 静安新城九区
-- 静安新城二区
-- 静安新城五区
-- 静安新城八区
-- 静安新城十一区
-- 静安新城十二区
-- 静安新城十区
-- 静安新城四区

-- 成交价走势(静安新城-各区)
select 
    `date`,
    ifnull(round(jinan1_price/jinan1_count,2), 0),
    ifnull(round(jinan7_price/jinan7_count,2), 0),
    ifnull(round(jinan3_price/jinan3_count,2), 0),
    ifnull(round(jinan9_price/jinan9_count,2), 0),
    ifnull(round(jinan2_price/jinan2_count,2), 0),
    ifnull(round(jinan5_price/jinan5_count,2), 0),
    ifnull(round(jinan8_price/jinan8_count,2), 0),
    ifnull(round(jinan11_price/jinan11_count,2), 0),
    ifnull(round(jinan12_price/jinan12_count,2), 0),
    ifnull(round(jinan10_price/jinan10_count,2), 0),
    ifnull(round(jinan4_price/jinan4_count,2), 0)
from (
    select 
        DATE_FORMAT(transaction_time,'%Y-%m') as 'date', 
        sum(case area_name when '静安新城一区' then unit_price/10000 else 0 end) as 'jinan1_price',
        sum(case area_name when '静安新城七区' then unit_price/10000 else 0 end) as 'jinan7_price',
        sum(case area_name when '静安新城三区' then unit_price/10000 else 0 end) as 'jinan3_price',
        sum(case area_name when '静安新城九区' then unit_price/10000 else 0 end) as 'jinan9_price',
        sum(case area_name when '静安新城二区' then unit_price/10000 else 0 end) as 'jinan2_price',
        sum(case area_name when '静安新城五区' then unit_price/10000 else 0 end) as 'jinan5_price',
        sum(case area_name when '静安新城八区' then unit_price/10000 else 0 end) as 'jinan8_price',
        sum(case area_name when '静安新城十一区' then unit_price/10000 else 0 end) as 'jinan11_price',
        sum(case area_name when '静安新城十二区' then unit_price/10000 else 0 end) as 'jinan12_price',
        sum(case area_name when '静安新城十区' then unit_price/10000 else 0 end) as 'jinan10_price',
        sum(case area_name when '静安新城四区' then unit_price/10000 else 0 end) as 'jinan4_price',
        sum(case area_name when '静安新城一区' then 1 else 0 end) as 'jinan1_count',
        sum(case area_name when '静安新城七区' then 1 else 0 end) as 'jinan7_count',
        sum(case area_name when '静安新城三区' then 1 else 0 end) as 'jinan3_count',
        sum(case area_name when '静安新城九区' then 1 else 0 end) as 'jinan9_count',
        sum(case area_name when '静安新城二区' then 1 else 0 end) as 'jinan2_count',
        sum(case area_name when '静安新城五区' then 1 else 0 end) as 'jinan5_count',
        sum(case area_name when '静安新城八区' then 1 else 0 end) as 'jinan8_count',
        sum(case area_name when '静安新城十一区' then 1 else 0 end) as 'jinan11_count',
        sum(case area_name when '静安新城十二区' then 1 else 0 end) as 'jinan12_count',
        sum(case area_name when '静安新城十区' then 1 else 0 end) as 'jinan10_count',
        sum(case area_name when '静安新城四区' then 1 else 0 end) as 'jinan4_count'
    from lianjia where transaction_time >= '2015-01-01' and area_name like '静安新城%' group by DATE_FORMAT(transaction_time,'%Y-%m')
) t

-- 成交周期
select 
    DATE_FORMAT(transaction_time,'%Y-%m'),
    sum(case when duration > 0 and duration <= 30 then 1 else 0 end) as '0-30',
    sum(case when duration > 30 and duration <= 60 then 1 else 0 end) as '30-60',
    sum(case when duration > 60 and duration <= 90 then 1 else 0 end) as '60-90',
    sum(case when duration > 90 and duration <= 180 then 1 else 0 end) as '90-180',
    sum(case when duration > 180 then 1 else 0 end) as '180-',
from lianjia where transaction_time >= '2015-01-01'  and area_name like '静安新城%' group by DATE_FORMAT(transaction_time,'%Y-%m')

-- 交易差额
select DATE_FORMAT(transaction_time,'%Y-%m'), round(avg(sticker_price-transaction_price)) from lianjia where transaction_time >= '2015-01-01'  and area_name like '静安新城%' and transaction_price>0 group by DATE_FORMAT(transaction_time,'%Y-%m')


-- 闵行第一梯队 明强小学&闵实验
-- 闵行区实验小学：莘沥 莘松五村、莘松三村、莘松八村、锦澳花园、莘松九村、锦都花苑、银厦花园、裕兴花园、明物大厦、莘怡公寓
-- 闵行区实验小学春城校区：伟业路、水仙苑、玉兰苑、随园、万科假日风景、上海春城、绿地春申、莘南花苑、江南名邸、新空间、茉莉苑、玫瑰九九
-- 闵行区实验小学畹町校区：高兴花园、中城绿苑、常兴家园、莲花新村、春馨苑、行西村、集心村
-- 闵行区实验小学景城校区：集心路、春申景城
-- 闵行区七宝镇明强小学：七宝村、友谊村、三佳花园、茂盛花园、水景书香园、宝仪花园、学院新村、东方花园、莲浦府邸、皇都花园、明泉公寓、蒲汇别墅、蒲汇新村、京都苑、白浪新村、塘北居委所属小区（北大街、北东街、北西街、青年路、青南小区、民主路、民主新村、横沥新村、北横沥、北东塘滩、沟水弄等，除吴宝路27弄外）、塘南居委所属小区（王家场、南大街、南街、南西街、南东街、南东塘滩、南西塘滩、竹行弄、浴堂街、富强街、镇企路、南横沥等）、华夏名苑、宝隆新村、农学院家属小区、秀枫翠谷、金泰公寓、红明、九星村、江南御府
select * from lianjia where transaction_time >= '2017-01-01' and
-- 闵行区实验小学：
(area_name like '莘沥%' or area_name like '莘松五村%' or area_name like '莘松三村%' or area_name like '莘松八村%' or area_name like '锦澳花园%' or area_name like '莘松九村%' or area_name like '锦都花苑%' or area_name like '银厦花园%' or area_name like '裕兴花园%' or area_name like '明物大厦%' or area_name like '莘怡公寓%'
-- 闵行区实验小学春城校区： 
or area_name like '伟业路%' or area_name like '水仙苑%' or area_name like '玉兰苑%' or area_name like '随园%' or area_name like '万科假日风景%' or area_name like '上海春城%' or area_name like '绿地春申%' or area_name like '莘南花苑%' or area_name like '江南名邸%' or area_name like '新空间%' or area_name like '茉莉苑%' or area_name like '玫瑰九九%'
-- 闵行区实验小学畹町校区：
 or area_name like '高兴花园%' or area_name like '中城绿苑%' or area_name like '常兴家园%' or area_name like '莲花新村%' or area_name like '春馨苑%' or area_name like '行西村%'
or area_name like '集心%'
-- 闵行区实验小学景城校区：
or area_name like '集心%' or area_name like '春申景城%'
-- 闵行区七宝镇明强小学：
 or area_name like '七宝村%' or area_name like '友谊村%' or area_name like '三佳花园%' or area_name like '茂盛花园%' or area_name like '水景书香园%' or area_name like '宝仪花园%' or area_name like '学院新村%' or area_name like '东方花园%' or area_name like '莲浦府邸%' or area_name like '皇都花园%' or area_name like '明泉公寓%' or area_name like '蒲汇别墅%' or area_name like '蒲汇新村%' or area_name like '京都苑%' or area_name like '白浪新村%' or area_name like '青南小区%' or area_name like '民主新村%' or area_name like '横沥新村%' or area_name like '竹行弄%' or area_name like '华夏名苑%' or area_name like '宝隆新村%' or area_name like '农学院家属小区%' or area_name like '秀枫翠谷%' or area_name like '金泰公寓%' or area_name like '红明%' or area_name like '九星村%' or area_name like '江南御府%'
)


