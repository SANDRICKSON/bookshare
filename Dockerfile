# Base image
FROM python:3.11-slim

# სამუშაო დირექტორია
WORKDIR /app

# საჭირო პაკეტების კოპირება და ინსტალაცია
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# პროექტის კოდის კოპირება
COPY . /app/

# პორტის ექსპოზიცია
EXPOSE 8000

# სერვერის გაშვება
CMD ["gunicorn", "bookshare.wsgi:application", "--bind", "0.0.0.0:8000"]
