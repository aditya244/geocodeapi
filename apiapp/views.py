from django.shortcuts import render
import requests
import openpyxl
def index(request):
    if "GET" == request.method:
         return render(request, 'index.html', {})
    else:
        excel_file = request.FILES["excel_file"]

        wb = openpyxl.load_workbook(excel_file)

        worksheet = wb["Sheet1"]
        print(worksheet)

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
                address = (cell.value)
                api_key = "AIzaSyDSVDzILhdxP3JuRElxyKfvfhbYRpIEmEs"
                api_response = requests.get(
                    'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
                api_response_dict = api_response.json()

                if api_response_dict['status'] == 'OK':
                    latitude = api_response_dict['results'][0]['geometry']['location']['lat']
                    longitude = api_response_dict['results'][0]['geometry']['location']['lng']

                row_data.append(str(longitude))
                row_data.append(str(latitude))
            excel_data.append(row_data)

    return render(request, 'index.html', {"excel_data": excel_data,'longitude':longitude,'latitude':latitude})