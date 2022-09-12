# airflow_reservoir
練習airflow怎麼運作，將資料運用網路爬蟲抓下，再利用airflow一步步存進mongo DB airflow要記得admin >> connections >> 將mongo DB設一個conn_id

dags下檔案為reservoir.py tasks有兩個檔案分別是collmongo.py及crawler.py crawler先去“https://fhyv.wra.gov.tw/FhyWeb/v1/Api/Reservoir/Visual?$format=JSON“ 抓取資料存進mongo，在跑cloomongo進行整理及重新儲存

crawler >> collmongo.t1 >>collmongo.t2 >>collmongo.t3
