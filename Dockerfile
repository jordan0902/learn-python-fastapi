FROM python:3.10.2

WORKDIR /usr/src/app

#optimise the process if only change the source code file. This step will be running only 
#when the requirement changes.
COPY requirements.txt ./

#install all the dependencies into app directory
RUN pip install --no-cache-dir -r requirements.txt

#copy everything in the source directory to the target directory
COPY . .

CMD ["uvicorn", "app.main:app","--host","0.0.0.0","--port","8000"]
