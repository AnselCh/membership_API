FROM python:3.9-slim-buster

# 複製本地端的檔案到容器內
COPY . /api

# 切換到工作目錄
WORKDIR /api

# 安裝相依套件
RUN pip install -r requirements.txt

# 開啟 8000 port
EXPOSE 8000

# 啟動 app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# 添加作者等其他訊息
LABEL maintainer="Ansel Chen <anannannan0102@gmail.com>"
LABEL version="1.0"
LABEL description="MemberSys FASTAPI"
