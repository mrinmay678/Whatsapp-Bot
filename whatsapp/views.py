from django.shortcuts import render
from django.http import HttpResponse
import csv
import time
from datetime import datetime

# Rest Framework Imports
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import webbrowser as web
import pyautogui as pg
import time

# Model and Serializers Imports
from .models import CSVFile, Contact
from .serializers import CSVModelSerializer


class UploadCsv(viewsets.ModelViewSet):
    queryset = CSVFile.objects.all()
    serializer_class = CSVModelSerializer


@api_view(['POST'])
def automate(request):
    Contact.objects.all().delete()
    browser = request.data['browser_name']
    dpath = request.data['dpath']
    message_type = request.data['message_type']
    obj = CSVFile.objects.get(used=False)
    obj.used = True
    obj.save()
    try:
        if browser == 'edge':
            driver = webdriver.Edge(dpath)
        elif browser == 'chrome':
            driver = webdriver.Chrome(dpath)
        elif browser == 'firefox':
            driver = webdriver.Firefox(dpath)
        elif browser == 'safari':
            driver = webdriver.Safari(dpath)
        else:
            return Response("Driver Error")
        driver.get("http://web.whatsapp.com/")

    except:
        return Response("Driver Problem ")

    wait = WebDriverWait(driver, 1000)


    if message_type == "tm":
        message = request.data['message']
        with open(obj.file_name.path, 'r') as f:
            read = csv.reader(f)
            for i, row in enumerate(read):
                name = row[0]
                try:
                    search_box = wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
                    search_box.send_keys(name+Keys.ENTER)
                except:
                    obj2 = Contact.objects.create(
                        phone=row[0], message=message, error="Search Box Not Found")
                    continue

                try:
                    input_box = wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')))
                    input_box.send_keys(message+Keys.ENTER)
                except:
                    obj2 = Contact.objects.create(
                        phone=row[0], message=message, error="User or Text Input Box Not Found")
                    continue

                current_time = datetime.now()
                timenow = str(current_time.strftime(
                    '%I'))+":"+str(current_time.strftime('%M'))+" "+str(current_time.strftime('%p'))
                obj2 = Contact.objects.create(
                    phone=row[0], message=message, time=timenow)

        return Response("Success")

    elif message_type == "ivm":
        message = request.data['message']
        file_path = request.data['file_path']
        with open(obj.file_name.path, 'r') as f:
            read = csv.reader(f)
            for i, row in enumerate(read):
                name = row[0]
                try:
                    search_box = wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
                    search_box.send_keys(name+Keys.ENTER)
                except:
                    obj2 = Contact.objects.create(
                        phone=row[0], message=message, file_send=file_path, error="Search Box Not Found")
                    continue

                try:
                    attach_box = wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="main"]/footer/div[1]/div[1]/div[2]')))
                    attach_box.click()
                except:
                    obj2 = Contact.objects.create(
                        phone=row[0], message=message, file_send=file_path, error="User Not Found")
                    continue

                try:
                    image_video_box = wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input')))
                    image_video_box.send_keys(file_path)
                except:
                    obj2 = Contact.objects.create(
                        phone=row[0], message=message, file_send=file_path, error="Image/Video Not Found")
                    continue

                try:
                    input_box = wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div[1]/span/div/div[2]/div/div[3]/div[1]/div[2]')))
                    input_box.send_keys(message)
                except:
                    obj2 = Contact.objects.create(
                        phone=row[0], message=message, file_send=file_path, error="Input Box Not Found")
                    continue

                current_time = datetime.now()
                timenow = str(current_time.strftime(
                    '%I'))+":"+str(current_time.strftime('%M'))+" "+str(current_time.strftime('%p'))
                try:
                    send_button = driver.find_element_by_xpath(
                        '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div')
                    send_button.click()
                except:
                    obj2 = Contact.objects.create(
                        phone=row[0], message=message, file_send=file_path, error="Send Button Not Found")
                    continue

                obj2 = Contact.objects.create(
                    phone=row[0], message=message, file_send=file_path, time=timenow)

        return Response("Success")

    elif message_type == "dm":
        file_path = request.data['file_path']
        with open(obj.file_name.path, 'r') as f:
            read = csv.reader(f)
            for i, row in enumerate(read):
                name = row[0]
                try:
                    search_box = wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
                    search_box.send_keys(name+Keys.ENTER)
                except:
                    obj2 = Contact.objects.create(
                        phone=row[0], file_send=file_path, error="Search Box Not Found")
                    continue

                try:
                    attach_box = wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="main"]/footer/div[1]/div[1]/div[2]')))
                    attach_box.click()
                except:
                    obj2 = Contact.objects.create(
                        phone=row[0], file_send=file_path, error="User Not Found")
                    continue

                try:
                    doc_box = wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div/div/ul/li[3]/button/input')))

                    doc_box.send_keys(file_path)
                except:
                    obj2 = Contact.objects.create(
                        phone=row[0], file_send=file_path, error="Document Not Found")
                    continue

                current_time = datetime.now()
                timenow = str(current_time.strftime(
                    '%I'))+":"+str(current_time.strftime('%M'))+" "+str(current_time.strftime('%p'))
                try:
                    send_button = wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div')))
                    send_button.click()
                except:
                    obj2 = Contact.objects.create(
                        phone=row[0], file_send=file_path, error="Send Button Not Found")
                    continue

                obj2 = Contact.objects.create(
                    phone=row[0], file_send=file_path, time=timenow)

        return Response("Success")

    else:
        return Response("Option Not Available Error")


@api_view(['POST'])
def trackRead(request):
    browser = request.data['browser_name']
    dpath = request.data['dpath']
    try:
        if browser == 'edge':
            driver = webdriver.Edge(dpath)
        elif browser == 'chrome':
            driver = webdriver.Chrome(dpath)
        elif browser == 'firefox':
            driver = webdriver.Firefox(dpath)
        elif browser == 'safari':
            driver = webdriver.Safari(dpath)
        else:
            return Response("Driver Error")
        driver.get("http://web.whatsapp.com/")

    except:
        return Response("Driver Problem ")

    wait = WebDriverWait(driver, 1000)
    rr = "Unread"
    time.sleep(5)
    for i in Contact.objects.filter(used=False).values_list('phone', 'message', 'time', 'error'):
        if i[3] == "":
            search_box = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
            search_box.send_keys("+"+i[0]+Keys.ENTER)
            div_2z = wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, '_2nWgr')))
            span_2z = div_2z.find_elements_by_tag_name(
                'span')
            for j in span_2z:
                rr = j.get_attribute('aria-label')
            if rr == " Read ":
                for k in Contact.objects.filter(phone=i[0]):
                    k.read_status = rr
                    k.used = True
                    k.save()
            else:
                for k in Contact.objects.filter(phone=i[0]):
                    k.read_status = "Unread"
                    k.used = False
                    k.save()


    driver.quit()

    return Response("You can download Sender Log Now")


def downloadCSV(request):
    response = HttpResponse(content_type="text/csv")
    writer = csv.writer(response)
    writer.writerow(['phone', 'time', 'error', 'read_status'])
    for i in Contact.objects.all():
        writer.writerow((i.phone, i.time, i.error, i.read_status))

    response['Content-Disposition'] = 'attachment; filename="sender_log.csv"'
    return response


def tracker(request):
    success_count = error_count = read_count = sb_error = u_error = iv_error = ib_error = sb_error = o_error = 0
    obj = Contact.objects.all()
    for object in obj:
        if object.error == "":
            success_count += 1
            if object.read_status == " Read ":
                read_count += 1
        else:
            error_count += 1
            if object.error == "Search Box Not Found":
                sb_error += 1
            elif object.error == "User Not Found" or object.error == "User or Text Input Box Not Found":
                u_error += 1
            elif object.error == "Image/Video Not Found":
                iv_error += 1
            elif object.error == "Input Box Not Found" or object.error == "User or Text Input Box Not Found":
                ib_error += 1
            elif object.error == "Send Button Not Found":
                sb_error += 1
            else:
                o_error += 1

    response = HttpResponse(content_type="text/csv")
    writer = csv.writer(response)
    writer.writerow(['Total Success', success_count])
    writer.writerow(['Total Error', error_count, ])
    writer.writerow(['Total Read', read_count])
    writer.writerow(['Search Box Not Found', sb_error])
    writer.writerow(['User Not Found', u_error])
    writer.writerow(['Image/Video Not Found', iv_error])
    writer.writerow(['Input Box Not Found', ib_error])
    writer.writerow(['Send Button Not Found', sb_error])
    writer.writerow([' Other', o_error])
    response['Content-Disposition'] = 'attachment; filename="success_error_log.csv"'
    return response


@api_view(['POST'])
def upload_unknown_csv_here(request):
    message = request.data['message']
    obj = CSVFile.objects.get(used=False)
    obj.used = True
    obj.save()
    with open(obj.file_name.path, 'r') as f:
        read = csv.reader(f)
        for i, row in enumerate(read):
            name = "+"+row[0]
            print(name)
            web.open("https://web.whatsapp.com/send?phone=" +
                        str(name)+"&text="+message)
            time.sleep(10)
            width, height = pg.size()
            pg.click(width/2, height/2)
            time.sleep(10)
            pg.press('enter')
            time.sleep(5)
            pg.hotkey('ctrl', 'w')
            time.sleep(5)
            current_time = datetime.now()
            timenow = str(current_time.strftime(
                '%I'))+":"+str(current_time.strftime('%M'))+" "+str(current_time.strftime('%p'))
            obj2 = Contact.objects.create(
                phone=row[0], message=message, time=timenow)

    return Response("Done")