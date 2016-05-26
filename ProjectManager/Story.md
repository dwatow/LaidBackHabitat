[admin]
動作	角色	任務
read	老闆	查詢訂單的付款狀況 -> 加上欄位: 訂單狀況
create	老闆	登錄招募的員工
create	老闆	登錄招募的房務員
create	老闆	輸入房型
create	老闆	輸入房間

[訂房前的查詢]
read	旅客	想知道加床的規則
read	旅客	想知道是不是有附早餐或其它附加服務
read	旅客	想知道民宿位置
read	旅客	想知道訂房的方法
~~read	旅客	想知道還有沒有空房~~ -> query_room/
read	旅客	想要查詢房型
read	旅客	會查詢一些民宿的最新消息(地方消息、折扣)
read	旅客	查詢附近景點簡單介紹
create	旅客	留言溫馨小語, 給民宿業者加油打氣

[訂房]
create	旅客	訂房+確定加值服務+是否加床
modify	旅客	告知已付訂金
modify	旅客	取消訂房

nodify	旅客	被系統告知尚未付訂金
nodify	旅客	被告知已取消訂房

[checkout]
動作	角色	任務
modify	服務生	幫客人辦理checkout -> 出現待打掃房間 -> 加上欄位: 房間狀態
read	房務員	查詢已checkout, 未打掃的房間

[checkin]
動作	角色	任務
modify	房務員	任務完成 -> 出現可checkin 房間
read	服務生	要查詢可checkin的房間
modify	服務生	幫客人checkin -> 收尾款

[未分類]
動作	角色	任務
create	旅客	想要客訴
modify	老闆	指派「待打掃房間」給房務員(也許不用每天)
read	服務生	查詢客人的訂單與加值服務

[無須實作]
動作	角色	任務
modify	旅客	checkin -> 結 尾款(服務生會幫旅客)
create	旅客	新增帳號(訂房時做這件事)
none	旅客	登入(實作在任何查詢)

[房務員要做的事(處理房間)]
[旅客	要做的事]
[服務生	要做的事(處理客人)]
[老闆	要做的事]
