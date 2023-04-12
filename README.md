code explain : __https://anselch.github.io/2023/03/15/fastapi/__

```
# 建立img
docker build -t mem_api .
# 啟動
docker run -p 8000:8000 --name memberapi mem_api
```

利用FAST API串接MongoBD

GET /membership/:得到DB內的所有資料
POST /membership/:建立會員資料
GET /membership/{account}:{account}內帶入要查詢的帳號
DELETE /membership/{account}:{account}內帶入要刪除的帳號
PATCH /membership/{account}:{account}內帶入要更新的帳號
最後前端使用AJAX操作POST方法建立會員資料。