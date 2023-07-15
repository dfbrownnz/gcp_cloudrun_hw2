
import os
import json
import pandas as pd

from flask import Flask, render_template, request
from algos import data_json 
from algos import data_buckets

app = Flask(__name__)

dj = data_json.c_data_json()
db = data_buckets.c_data_gbucket()
bucket_name='example-bucket-1-dfb'

template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# subfolders = [ f.path for f in os.scandir(template_dir) if f.is_dir() ]
# print(f'template_dir is {template_dir} {subfolders}')
# hard coded absolute path for testing purposes
# app = Flask(__name__, template_folder=template_dir)

@app.route("/")
def home():
    #name = os.environ.get("NAME", "World")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name='employee_records.json'
    print( dir_path + file_name)
    with open(dir_path + '/' + file_name, 'r', encoding='utf-8') as f_in_obj:
        jdata = json.load(f_in_obj)
    df = pd.DataFrame( data=jdata['employee'] )
    df.columns = dict(jdata['employee'][0] ).keys()
    return render_template( 'template.html', page_purpose_string=".", title="." , records  =  df.to_dict('records') , colnames = df.columns.values  )


@app.route("/json_read")
def json_read():
    #return_val =  dj.file_cwd()
    bucket_name='example-bucket-1-dfb'
    file_name='my_test.json'
    return_json= db.read_file_json(bucket_name , file_name)
    # print(f' type is {type(return_json["employee"])}    keys are {dict(return_json["employee"][0]).keys()} ')   #  and rows {return_json["employee"].items()} 
    #df = pd.DataFrame({ file_name:[return_json] })
    df = pd.DataFrame( data=return_json["employee"] )
    df.columns = dict(return_json["employee"][0]).keys()

    return render_template( 'template.html', page_purpose_string=".", title="." , records  =  df.to_dict('records') , colnames = df.columns.values  )


@app.route("/json_update")
def json_update():
    #return_val =  dj.file_cwd()
    bucket_name='example-bucket-1-dfb'
    file_name='my_test.json'
    return_json= db.read_file_json(bucket_name , file_name) # 

    # http://127.0.0.1:5000/json_update?username=Fred_creditCardDebt_CCLACBW027SBOG.csv
    #  https://8080-cs-957240302839-default.cs-us-east1-vpcf.cloudshell.dev/json_update?employee_name=Fred_creditCardDebt_CCLACBW027SBOG.csv
    # username = request.args.get('username')
    employee_name = request.args.get('employee_name')

    if employee_name is None:
        # blob_name='Financial_Report_tsla.xlsxConsolidated_Statements_Oper.csv'
        employee_name='Bobbb'
        print('json_update employee_name:', employee_name )
        return_json= db.read_file_json(bucket_name , file_name)
    else:
        print('json_update employee_name in none :', employee_name )
        for employee_record in return_json['employee']:
            print( f'c_datajson_update  {employee_record["id"] } ')
            if employee_record["id"]=='14':
                employee_record["name"]=employee_name
        db.write_file_json_data(bucket_name , file_name, return_json)
    # df = pd.DataFrame({ file_name:[return_json] })
    df = pd.DataFrame( data=return_json["employee"] )
    df.columns = dict(return_json["employee"][0]).keys()

    return render_template( 'template.html', page_purpose_string=".", title="." , records  =  df.to_dict('records') , colnames = df.columns.values  )


@app.route("/files")
def files():
    #return_val =  dj.file_cwd()
    # bucket_name='example-bucket-1-dfb'
    # db.write_file_json(bucket_name , 'my_test.json')
    # db.json_update(bucket_name , 'my_test.json')
    
    # return_json= db.read_file_json(bucket_name , 'my_test.json')
    # print( f'app route ->files-> return_json {return_json}')
    # db.test()
    # return_val = '<br>'+ db.meta_list_buckets()
    # return_val += '<br>'+ db.meta_list_blobs(bucket_name)
    # return f'<html> <a href="/"> Home </a>  <br>  <a href="/df"> df </a> <br> and load bucket<br>  <br>GCS {return_val} <br>return_json {return_json} </html>'

    #df = pd.DataFrame({ 'Type':[''] })
    #df['buckets Access'] =db.get_uniform_bucket_level_access( bucket_name) 
    #df['buckets'] =db.meta_list_buckets() # 
    #df['files'] =db.meta_list_blobs(bucket_name)
    #df['json'] = f'{return_json}'
    df = db.meta_list_blobs(bucket_name)
    #df = pd.DataFrame({ 'File Viewer':db.meta_list_blobs(bucket_name) })
    
    file_name=' route files '
    return render_template( 'template.html',page_purpose_string=".", title="." , records  =  df.to_dict('records') , colnames = df.columns.values  )



@app.route("/df_write")
def df_write():
    df = pd.DataFrame({ 'A':[1,2,3] })
    file_name=' file name '
    db.pandas_write(bucket_name , 'my_test.csv')
    return render_template( 'template.html', page_purpose_string=".", title="." , records  =  df.to_dict('records') , colnames = df.columns.values  )

@app.route("/df")
def df():
    # http://127.0.0.1:5000/df?folder_file_name=d:/
    # http://127.0.0.1:5000/df?file_name_csv=Fred_creditCardDebt_CCLACBW027SBOG.csv
    # https://8080-cs-957240302839-default.cs-us-east1-vpcf.cloudshell.dev/df?file_name_csv=tsla_all.csv
    # username = request.args.get('username')
    file_name_csv = request.args.get('file_name_csv')
    print('file_viewer:', file_name_csv )
    
    #return_val =  db.read_df()
    blob_name='Financial_Report_tsla.xlsxConsolidated_Statements_Oper.csv'
    if file_name_csv is None:
        # blob_name='Financial_Report_tsla.xlsxConsolidated_Statements_Oper.csv'
        print(' file_name_csv is none :', file_name_csv )
    else:
        print(' file_name_csv is none:', file_name_csv )
        blob_name=file_name_csv

    df = db.pandas_read(bucket_name, blob_name)

    #return '<html> <a href="/"> Home </a> <br>  <a href="/files">files </a> <br> and read xlsx from a bucket<br>  <br> file_cwd {}! </html>'.format(  return_val )
    return render_template( 'template.html', page_purpose_string=".", title="." , records  =  df.to_dict('records') , colnames = df.columns.values  )

@app.route("/a")
def a():
    return_val =  dj.read_example()
    # return '<html> <a href="/"> Home </a> from file <br> do new <br> is {}! </html>'.format(  return_val )
    df = pd.DataFrame({ 'A':[return_val] })
    file_name=' route a '
    return render_template( 'template.html', page_purpose_string=".", title="" , records  =  df.to_dict('records') , colnames = df.columns.values  )

@app.route("/about")
def about():
    return_val =  dj.read_example()
    # return '<html> <a href="/"> Home </a> from file <br> do new <br> is {}! </html>'.format(  return_val )
    df = pd.DataFrame({ 'A':[return_val] })
    file_name=' route about '
    return render_template( 'template.html', page_purpose_string=".", title="." , records  =  df.to_dict('records') , colnames = df.columns.values  )


if __name__== "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))