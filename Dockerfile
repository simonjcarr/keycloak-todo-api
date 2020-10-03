FROM python:3.7.4-stretch

RUN apt-get update \
&& apt-get install --yes unixodbc-dev \
&& pip install pyodbc==4.0.27
# --- Install Microsoft ODBC Driver
# https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Need some certificate fix to install msodbcsql17
RUN apt-get install --yes apt-transport-https ca-certificates \
&& apt-get update && ACCEPT_EULA=Y apt-get install --yes msodbcsql17

WORKDIR /app



COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app
EXPOSE 8000
CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]