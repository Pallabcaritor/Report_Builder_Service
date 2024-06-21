from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
import psycopg2
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .helper import generate_query, config_str_to_list
from .queries import REALTION_MASTER_QUERY
#from django.core.paginator import Paginator
#import json
from django.http import JsonResponse
from .models import ApplicationUser, TableRelationMaster

#connection = psycopg2.connect(database="pfmegrnargs", user="reader", password="NWDMCE5xdipIjRrp", host="hh-pgsql-public.ebi.ac.uk", port=5432)
#connection = psycopg2.connect(database="ashirvad", user="ashirvad", password="password", host="localhost", port=5432)
#connection = psycopg2.connect(database="booking-backoffice", user="username", password="dsnjdk73bjdn", host="123.2422.23.142", port=6541)
connection = psycopg2.connect(database="asics", user="asics", password="password", host="localhost", port=5432)
#connection = psycopg2.connect(database="asics", user="postgres", password="ashwaq", host="localhost", port=5432)

cursor = connection.cursor()
# Create your views here.

def home(request):
    if request.method == 'POST':
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(request, username=uname, password=pwd)
        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in...")
            return redirect('home')
        else:
            messages.success(request, "There is an error logging in. Please try again..")
            return redirect('home')
    else:
        return render(request, 'home.html', {})

# def login_users(request):
#     pass

def logout_users(request):
    logout(request)
    messages.success(request, "You have been logged out....")
    return redirect('home')

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def getschemas(request):
    
    try:
        cursor.execute("SELECT schema_name FROM information_schema.schemata;")

        record = cursor.fetchall()
        schemas = []
        for sc in record:
            schemas.append(sc[0])

        return Response({"schemas" : schemas},status=status.HTTP_200_OK)
    except Exception as e:
        Response({'error': str(e)} , status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def gettablesbyschema(request):
    
    if 'schema' in request.GET:
        schema = request.GET['schema']
    else:
        return Response({'error': 'Please send schema name in params'} , status=status.HTTP_400_BAD_REQUEST)
    
    try:
        cursor.execute(f"SELECT * FROM information_schema.tables WHERE table_schema ='{schema}';")

        record = cursor.fetchall()
        tables_name = []
        for ta in record:
            tables_name.append(str(ta[2]))

        return Response({"tables" : tables_name},status=status.HTTP_200_OK)
    except Exception as e:
        Response({'error': str(e)} , status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def getcolumnsoftable(request):

    data = request.data
    if 'schema' in request.GET:
    #and 'table1' in request.GET:
        schema = request.GET['schema']
    #    table1 = request.GET['table1']
    else:
        #return Response({'error': 'Please send schema & table1 name in params'} , status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Please send schema name in params'} , status=status.HTTP_400_BAD_REQUEST)

    
    """if 'table2' in request.GET:
        table2 = request.GET['table2']
    if 'table3' in request.GET:
        table3 = request.GET['table3']"""
    
    tables_param = request.GET['tables']
    tables = config_str_to_list(tables_param)
    print(tables)
    tblen = len(tables)
    # if tblen == 3:
    #     table1 = tables[0]
    #     table2 = tables[1]
    #     table3 = tables[2]
    # elif tblen == 2:
    #     table1 = tables[0]
    #     table2 = tables[1]
    #     table3 = None
    # elif tblen == 1:
    #     table1 = tables[0]
    #     table2 = None
    #     table3 = None
    # else:
    #     table1 = None
    #     table2 = None
    #     table3 = None
    #tables[2]
    response_dic = []
    try:
        for tb in tables:
            cursor.execute(f"SELECT * FROM information_schema.columns WHERE table_schema = '{schema}' AND table_name = '{tb}';")

            record1 = cursor.fetchall()
            columns = []
            for ta in record1:
                columns.append(str(ta[3]))
            response_dic.append({"table": str(tb),"columns": columns})     
        return Response(response_dic,status=status.HTTP_200_OK)
    except Exception as e:
        Response({'error': str(e)} , status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def fetchdata(request):
    
        # if 'schema' in request.GET and 'table' in request.GET and 'page' in request.GET:
        #     schema = request.GET['schema']
        #     table = request.GET['table']
        # else:
        #     return Response({'error': 'Please send schema & table name and page number in params'} , status=status.HTTP_400_BAD_REQUEST)
        
        # data = request.data
        # page = request.GET['page']

        # items_per_page = 50
        # offset = (int(page) - 1) * items_per_page

        # query = generate_query(data, schema, table, offset)
        if 'q' in request.GET:
            query = request.GET['q']
        #print("Query--->",query)
        cursor.execute(query)        
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))
        final_results = {}
        # final_results['page_number'] = page
        final_results['per_page'] = 50
        final_results['records'] = results

        return JsonResponse([final_results], safe=False)
        # json_data = json.dumps(results)
        # print(json_data)

        # response = Paginator([], 50)
        # if int(page) > int(response.num_pages):
        #     return Response("NO data in this page!",status=status.HTTP_400_BAD_REQUEST)
        # print(type(response.page(page)))
        # res_data ={}
        # res_data['page_no'] = page
        # res_data['count'] = str(response.count)
        # res_data['pages'] = str(response.num_pages)
        # res_data['per_page'] = 50
        # res_data['results'] = str(response.page(page))

        
        #return Response(res_data,status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def populate_relation(request):
    if 'schema' in request.GET:
        schema = request.GET['schema']
        if len(schema) == 0 or schema is None:
            return Response({'error': 'Please provide schema name'} , status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Please send schema name in params'} , status=status.HTTP_400_BAD_REQUEST)

    cursor.execute(REALTION_MASTER_QUERY)        
    #columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    appid = ApplicationUser.objects.first()
    TableRelationMaster.objects.all().delete()
    try:
        for row in rows:
            values = {
                "schema" : schema,
                "appuserid" : appid, 
                "table_name" : str(row[1]),
                "column_name" : str(row[2]),
                "foreign_table_name" : str(row[3]),
                "foreign_column_name" : str(row[4]),
                "child_data_type" : str(row[5]),
                "parent_data_type" : str(row[6])
                }
            tbObj = TableRelationMaster(**values)
            tbObj.save()
    except Exception as e:
        Response({'error': str(e)} , status=status.HTTP_400_BAD_REQUEST)

    return Response({"OK"},status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_related_tables(request):
    if 'schema' in request.GET and 'tables' in request.GET:
        schema = request.GET['schema']
        table = request.GET['tables']
        #table = config_str_to_list(table)
        table = table.split()
        print(table)
        if len(schema) == 0 or schema is None:
            return Response({'error': 'Please provide schema name'} , status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Please send schema name in params'} , status=status.HTTP_400_BAD_REQUEST)
    
    related_obj = TableRelationMaster.objects.filter(table_name=table[0]).all()
    print(related_obj)
    for_table = []
    for ft in related_obj:
        for_table.append(ft.foreign_table_name)
    #for_table = ['table1', 'table2','table3']
    rel_data = {"parent_table": str(table[0]),"foreign_table": for_table}
    return Response(rel_data, status=status.HTTP_200_OK)

