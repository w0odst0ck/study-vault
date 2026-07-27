-- 1. 用户表 `user_info`
-- user_id,user_name,sex,age,register_time
-- 2. 订单表 `order_info`
-- order_id,user_id,order_amount,pay_time,order_status/（0 未支付 1 已支付 2 已取消）
-- 3. 行为日志表 `user_behavior`
-- id,user_id,event_type/（浏览 / 加购 / 下单 / 支付）,create_time

-- 按 18 岁以下、18-25、26-35、35 以上 统计人数
SELECT 
    CASE
        WHEN age < 18 THEN '18岁以下'
        WHEN age BETWEEN 18 AND 25 THEN '18-25岁'
        WHEN age BETWEEN 26 AND 35 THEN '26-35岁'
        ELSE '35岁以上'
    END AS age_group,
    COUNT(user_id) AS user_cnt
FROM user_info
GROUP BY age_group;

-- 取每个用户最新的已支付订单
SELECT * 
FROM(
    SELECT 
        *,
        ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY pay_time DESC) AS rn
    FROM order_info
    WHERE order_state =1
) t
WHERE rn =1;

-- 统计每日下单用户数、支付用户数、下单金额
SELECT
    DATE(pay_time) AS dt,
    COUNT(DISTINCT user_id) AS order_cnt,
    COUNT(DISTINCT CASE WHEN order_state =1 THEN user_id END) AS pay_user_cnt,
    SUM(CASE WHEN order_state =1 THEN order_amount ELSE 0 END) AS total_pay_amount
FROM order_info
GROUP BY DATE(pay_time);

-- 找出连续 3 天都有下单的用户
WITH t AS(
    SELECT
        user_id,
        DATE(pay_time) AS dt,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY DATE(pay_time)) AS rn
    FROM order_info
    GROUP BY user_id,DATE(pay_time)
)
SELECT DISTINCT user_id
FROM t
GROUP BY user_id,DATE_SUB(dt,INTERVAL rn DAY)
HAVING COUNT(*) >=3;

-- 手机号、身份证数据脱敏
SELECT CONCAT(SUBSTR(phone,1,3),'****',SUBSTR(phone,8,4)) AS phone_mask
SELECT CONCAT(SUBSTR(id_card,1,6),'********',SUBSTR(id_card,15,4)) AS id_mask

-- 删除重复数据，保留 id 最小的一条
DELETE t1 FROM user_behavior t1
JOIN user_behavior t2
ON t1.user_id = t2.user_id
AND t1.event_type = t2.event_type
AND t1.id > t2.id;
CREATE INDEX idx_user_event ON user_behavior (user_id, event_type, id);

DELETE FROM user_behavior
WHERE id NOT IN (
    SELECT
        MIN(id)
    FROM user_behavior
    GROUP BY user_id,event_type
);

-- 一行展示 浏览次数、加购次数、下单次数
SELECT 
    user_id,
    SUM(IF(event_type='浏览',1,0)) AS view_cnt,
    SUM(IF(event_type='加购',1,0)) AS cart_cnt,
    SUM(IF(event_type='下单',1,0)) AS order_cnt
FROM user_behavior
GROUP BY user_id;

SELECT
    user_id,
    SUM(CASE WHEN event_type = '浏览' THEN 1 ELSE 0 END) AS view_cnt,
    SUM(CASE WHEN event_type = '加购' THEN 1 ELSE 0 END) AS cart_cnt,
    SUM(CASE WHEN event_type = '下单' THEN 1 ELSE 0 END) AS order_cnt
FROM user_behavior
GROUP BY user_id;

-- 分页优化
SELECT * FROM order_info LIMIT 100000,10;
SELECT t.* FROM order_info t 
JOIN (SELECT id FROM order_info ORDER BY id LIMIT 100000,10) tmp 
ON t.id = tmp.id
ORDER BY t.id;

-- # 第二部分：Hive 数仓手撕 SQL（10 道面试必考）
-- `dwd_user_behavior_d`：用户行为明细分区表，dt 分区
-- `dwd_order_info_d`：订单明细分区表
-- `dim_user_zip`：用户拉链维度表

-- 每日 UV、PV、新用户数
SELECT 
    dt,
    COUNT(*) AS pv ,
    COUNT(DISTINCT user_id) AS uv ,
    COUNT(DISTINCT CASE WHEN first_login_dt=dt THEN user_id END) AS new_user_cnt
FROM dwd_user_behavior_d
GROUP BY dt;

-- 窗口函数排名：每日下单金额 TOP3 用户
WITH t AS (
    SELECT
        dt,
        user_id,
        SUM(order_amount) AS user_amount,
        ROW_NUMBER() OVER(PARTITION BY dt ORDER BY SUM(order_amount) DESC) AS rn 
    FROM dwd_order_info_d
    WHERE dt = '2026-05-05'
    GROUP BY dt, user_id  -- 分组必须包含 dt
)
SELECT *
FROM t 
WHERE rn <= 3;

-- 用户 7 日留存率（面试必背）
WITH user_first AS(
    SELECT
        user_id,
        MIN(dt) AS first_dt
    FROM dwd_user_behavior_d
    GROUP BY user_id
)
SELECT
    first_dt,
    COUNT(DISTINCT uf.user_id) AS new_user,
    COUNT(DISTINCT ub.user_id) AS retain_7d_user,
    ROUND(COUNT(DISTINCT ub.user_id)/COUNT(DISTINCT ub.user_id),4) AS retain_rate
FROM user_first uf 
LEFT JOIN dwd_user_behavior_d ub 
ON uf.user_id = ub.user_id
AND ub.dt = DATE_ADD(uf.dt,7)
GROUP BY first_dt;

-- 行为漏斗分析：浏览→加购→下单→支付转化率
SELECT 
    COUNT(DISTINCT CASE WHEN event_type = '浏览' THEN user_id END) AS view_user,
    COUNT(DISTINCT CASE WHEN event_type = '加购' THEN user_id END) AS cart_user,
    COUNT(DISTINCT CASE WHEN event_type = '下单' THEN user_id END) AS order_user,
    COUNT(DISTINCT CASE WHEN event_type = '支付' THEN user_id END) AS pay_user，
    ROUND(COUNT(DISTINCT CASE WHEN event_type = '加购' THEN user_id END)/
    COUNT(DISTINCT CASE WHEN event_type = '浏览' THEN user_id END),4) AS view2cart_rate
FROM dwd_user_behavior_d
WHERE dt='2026-05-05'

-- Hive 去重标准写法
INSERT OVERWRITE TABLE dwd_user_behavior_d PARTITION(dt='2026-05-05')
WITH t AS (
    SELECT
        user_id,
        event_type,
        create_time,
        ROW_NUMBER() OVER(
            PARTITION BY user_id, event_type 
            ORDER BY create_time DESC
        ) AS rn
    FROM ods_user_behavior_log
    WHERE dt = '2026-05-05'
)
SELECT
    user_id,
    event_type,
    create_time
FROM t
WHERE rn = 1;

-- 拉链表 SCD2 核心手撕 SQL（用户维度历史回溯）
INSERT OVERWRITE TABLE dim_user_zip
SELECT
    user_id,
    user_name,
    user_level,
    start_date,
    DATE_ADD('2026-05-05',-1) AS end_date,
    0 AS is_current
FROM dim_user_zip
WHERE is_current = 1
UNION ALL
SELECT
    user_id,user_name,user_level,
    '2026-05-05' AS start_date,
    '9999-12-31' AS end_date,
    1 AS is_current
FROM dwd_user_info_d
WHERE dt='2026-05-05'; 

-- Hive 数据倾斜 加盐打散 标准手撕 SQL
SELECT
    user_id,
    SUM(pv) AS total_pv
FROM (
    SELECT
        user_id,
        CONCAT(user_id,'_',FLOOR(RAND()*10)) AS user_key,
        COUNT(*) AS pv
    FROM dwd_user_behavior_d
    WHERE dt = '2026_05_05'
    GROUP BY user_id,CONCAT(user_id,'_',FLOOR(RAND()*10))
) t1
GROUP BY user_id;

-- 列转行（炸裂函数 lateral view explode）
SELECT
    user_id,
    tag
FROM dwd_user_tag_d
LATERAL VIEW explode(split(tag_list,',')) tmp AS tag
WHERE dt='2026_05_05'

-- 行转列 拼接字符串
SELECT
    user_id,
    concat_ws(',',collect_set(event_type)) AS event_list
FROM dwd_user_behavior_d
WHERE dt='2026_05_05'
GROUP BY user_id;

-- 小文件合并 Hive 常用配置（面试默写）
set hive.merge.mapfiles = true;
set hive.merge.mapredfiles = true;
set hive.merge.size.per.task = 268435456;
set hive.merge.smallfiles.avgsize = 134217728;

-- 1. `dwd_production` 生产明细表
-- `workshop_id,product_id,dt,total_num,good_num`（车间 ID、产品 ID、日期、总产量、合格量）
-- 2. `dwd_order` 订单明细表
-- `product_id,order_dt,order_num,deliver_num,status`（产品 ID、订单日期、订单量、发货量、状态：2 = 有效）
-- 3. `dim_product` 产品维度表
-- `product_id,product_name,type`（产品 ID、名称、类型）
-- 4. `dim_workshop` 车间维度表
-- `workshop_id,workshop_name`（车间 ID、名称）

-- 题目 1：基础业务统计（30 分）
--- 统计 **2024-11 月份** 每个车间、每个产品的：
-- 车间名称、产品名称、产品类型
-- 总产量、合格量、合格率（保留 4 位小数）
过滤条件：总产量≥500，按合格率降序排序
SELECT
  w.workshop_name,
  p.product_name,
  p.type,
  SUM(pro.total_num) AS total_num,
  SUM(pro.good_num) AS good_num,
  ROUND(SUM(pro.good_num)/SUM(pro.total_num),4) AS pass_rate
FROM dwd_production pro
JOIN dim_workshop w ON pro.workshop_id = w.workshop_id
JOIN dim_product p ON pro.product_id = p.product_id
WHERE pro.dt BETWEEN '2024-11-01' AND '2024-11-30'
GROUP BY w.workshop_name,p.product_name,p.type
HAVING SUM(pro.total_num)>=500
ORDER BY pass_rate DESC;

-- 题目 2：窗口函数业务实战（35 分）
-- 基于生产表，统计**每个车间每日**数据：
-- 1. 当日总产量、当日合格率
-- 2. 昨日合格率（LAG）
-- 3. 合格率环比变化率
-- 4. 车间当日产量排名（同车间内按日期排序）
-- 输出：车间名称、日期、当日产量、合格率、昨日合格率、环比、排名
WITH t1 AS (
  SELECT
    w.workshop_name,
    pro.dt,
    SUM(pro.total_num) AS daily_total,
    ROUND(SUM(pro.good_num)/SUM(pro.total_num),4) AS daily_pass
  FROM dwd_production pro
  JOIN dim_workshop w ON pro.workshop_id=w.workshop_id
  GROUP BY w.workshop_name,pro.dt
)
SELECT
  workshop_name,
  dt,
  daily_total,
  daily_pass,
  LAG(daily_pass,1) OVER(PARTITION BY workshop_name ORDER BY dt) AS last_pass,
  ROUND((daily_pass - LAG(daily_pass,1) OVER(PARTITION BY workshop_name ORDER BY dt))/LAG(daily_pass,1) OVER(PARTITION BY workshop_name ORDER BY dt),4) AS change_rate,
  RANK() OVER(PARTITION BY workshop_name ORDER BY daily_total DESC) AS rk
FROM t1
ORDER BY workshop_name,dt;

-- 题目 3：复杂业务综合手撕（35 分）
-- 联动生产 + 订单 + 产品表，统计 2024-11 月**各产品**业务指标：
-- 1. 生产总量、有效订单量、发货量
-- 2. 订单履约率 = 发货量 / 订单量（保留 4 位）
-- 3. 库存缺口 = 订单量 - 生产量（负数则为 0）
-- 4. 同产品类型的平均履约率
-- 过滤：排除产品类型 =`耗材`，按履约率降序
WITH pro_t AS (
  SELECT product_id,SUM(total_num) AS pro_total
  FROM dwd_production WHERE dt BETWEEN '2024-11-01' AND '2024-11-30'
  GROUP BY product_id
),
order_t AS (
  SELECT product_id,SUM(order_num) AS order_total,SUM(deliver_num) AS deliver_total
  FROM dwd_order WHERE order_dt BETWEEN '2024-11-01' AND '2024-11-30' AND status=2
  GROUP BY product_id
),
type_t AS (
  SELECT p.type,ROUND(AVG(CASE WHEN o.order_total>0 THEN o.deliver_total/o.order_total END),4) AS avg_rate
  FROM dim_product p
  LEFT JOIN order_t o ON p.product_id=o.product_id
  GROUP BY p.type
)
SELECT
  p.type,
  p.product_name,
  COALESCE(pt.pro_total,0) AS pro_total,
  COALESCE(ot.order_total,0) AS order_total,
  COALESCE(ot.deliver_total,0) AS deliver_total,
  CASE WHEN ot.order_total>0 THEN ROUND(ot.deliver_total/ot.order_total,4) END AS fulfill_rate,
  GREATEST(ot.order_total - pt.pro_total,0) AS gap,
  tt.avg_rate
FROM dim_product p
LEFT JOIN pro_t pt ON p.product_id=pt.product_id
LEFT JOIN order_t ot ON p.product_id=ot.product_id
LEFT JOIN type_t tt ON p.type=tt.type
WHERE p.type!='耗材'
ORDER BY fulfill_rate DESC;


