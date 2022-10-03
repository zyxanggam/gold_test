#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import sqlite3
import pandas as pd
from flask import Flask, jsonify, request, make_response
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

data_base=sqlite3.connect('data.db', check_same_thread=False)
data_base.row_factory = sqlite3.Row
mycursor = data_base.cursor()
data_base.execute('''CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT, old_text varchar(255), new_text varchar(255));''')

SWAGGER_URL ='/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name':"Text Cleansing Abusive Word"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

#welcomepage
@app.route('/', methods=['GET'])
def get():
  return "Welcome to Text Cleansing Abusive Word!"

#data get dan post
@app.route("/data", methods=["GET","POST"])
def data():
  if request.method == "POST":
    text = str(request.form["text"])
    df = pd.read_csv(r'C:\Users\User\Documents\binar\Python\binar-academy\hint\filter_data.csv')
    filtertext = df.abusive.to_list()
    filter1 = re.sub('([^\x00-\x7f])|(USER)|(@[A-Za-z0-9_]+)|(#[A-Za-z0-9_]+)|(RT)','',text)
    filter2 = re.sub(r'([^\w\s])|(\n)',' ',filter1)
    filter3 = re.sub('&amp;','dan',filter2)
    filter4 = re.sub(' +',' ',filter3)
    filter5 = filter4.lower()
    textOK = filter5.strip()
    
    word_split = textOK.split()
    abs_word = ([word for word in textOK.split() if word in filtertext])
    abs_word_count = len(abs_word)
    
    def text_sensor(a):
        if abs_word_count == 1 :
            abs1 = [abs_word[0]]
            for ac in abs1 :
                nameregex = re.compile(r'(\w)\w*')
                ab = nameregex.sub(r'\1****',ac)
            for ad in ab :
                ad = re.sub(ac,ab,a)
            return ad
        
        elif abs_word_count == 2 :
            abs1 = [abs_word[0]]
            abs2 = [abs_word[1]]
    
            for ac in abs1 :
                nameregex = re.compile(r'(\w)\w*')
                ab = nameregex.sub(r'\1****',ac)
            for ad in ab :
                ad = re.sub(ac,ab,a)
            for ae in abs2 :
                nameregex = re.compile(r'(\w)\w*')
                af = nameregex.sub(r'\1****',ae)
            for ag in af :
                ag = re.sub(ae,af,ad)
            return ag
        
        elif abs_word_count == 3 :
            abs1 = [abs_word[0]]
            abs2 = [abs_word[1]]
            abs3 = [abs_word[2]]
    
            for ac in abs1 :
                nameregex = re.compile(r'(\w)\w*')
                ab = nameregex.sub(r'\1****',ac)
            for ad in ab :
                ad = re.sub(ac,ab,a)
    
            for ae in abs2 :
                nameregex = re.compile(r'(\w)\w*')
                af = nameregex.sub(r'\1****',ae)        
            for ag in af :
                ag = re.sub(ae,af,ad)
    
            for ah in abs3 :
                nameregex = re.compile(r'(\w)\w*')
                ai = nameregex.sub(r'\1****',ah)
            for aj in ai :
                ak = re.sub(ah,ai,ag)    
            return ak
        
        elif abs_word_count == 4 :
            abs1 = [abs_word[0]]
            abs2 = [abs_word[1]]
            abs3 = [abs_word[2]]
            abs4 = [abs_word[3]]

            for ac in abs1 :
                nameregex = re.compile(r'(\w)\w*')
                ab = nameregex.sub(r'\1****',ac)
            for ad in ab :
                ad = re.sub(ac,ab,a)

            for ae in abs2 :
                nameregex = re.compile(r'(\w)\w*')
                af = nameregex.sub(r'\1****',ae)
            for ag in af :
                ag = re.sub(ae,af,ad)
    
            for ah in abs3 :
                nameregex = re.compile(r'(\w)\w*')
                ai = nameregex.sub(r'\1****',ah)
            for aj in ai :
                ak = re.sub(ah,ai,ag)  
    
            for al in abs4 :
                nameregex = re.compile(r'(\w)\w*')
                am = nameregex.sub(r'\1****',al)
            for an in am :
                ao = re.sub(al,am,ak)
            return ao
        
        elif abs_word_count > 4 :
            ap = 'kalimat terlalu abusive'
            return ap
    
        else :
            textOK
            
        return str(a)
    
    text_clean = text_sensor(textOK)
    
    query_text = "insert into data(old_text,new_text) values(?,?)"
    val = (text, text_clean)
    mycursor.execute(query_text, val)
    data_base.commit()
    print(text)
    print(text_clean)
    return "Sukses untuk menginput data"

  elif request.method == "GET":
    query_text = "select * from data"
    select_data = mycursor.execute(query_text)
    data=[
        dict(id=row[0], old_text=row[1], new_text=row[2])
        for row in select_data.fetchall()
    ]
    return jsonify(data)


#data get, put dan delete
@app.route("/data/<string:id>", methods=["GET","PUT","DELETE"])   
def id(id):
  if request.method =="GET":
    query_text = "select * from data where id = ?"
    val = str(id)
    select_data = mycursor.execute(query_text,[val])
    data=[
        dict(id=row[0],old_text=row[1], new_text=row[2])
        for row in select_data.fetchall()
    ] 
    print(data)
    return jsonify(data)

  elif request.method =="DELETE":
    query_text = "delete from data where id = ?"
    val = id
    mycursor.execute(query_text,[val])
    data_base.commit()
    return "Data berhasil dihapus"

  elif request.method == "PUT":
    text = str(request.form["text"])
    
    # ganti directory untuk lokasi file abusive word
    df = pd.read_csv(r'C:\Users\User\Documents\binar\Python\binar-academy\hint\filter_data.csv')
    filtertext = df.abusive.to_list()
    filter1 = re.sub('([^\x00-\x7f])|(USER)|(@[A-Za-z0-9_]+)|(#[A-Za-z0-9_]+)|(RT)','',text)
    filter2 = re.sub(r'([^\w\s])|(\n)',' ',filter1)
    filter3 = re.sub('&amp;','dan',filter2)
    filter4 = re.sub(' +',' ',filter3)
    filter5 = filter4.lower()
    textOK = filter5.strip()
    
    word_split = textOK.split()
    abs_word = ([word for word in textOK.split() if word in filtertext])
    abs_word_count = len(abs_word)
    
    def text_sensor(a):
        if abs_word_count == 1 :
            abs1 = [abs_word[0]]
            for ac in abs1 :
                nameregex = re.compile(r'(\w)\w*')
                ab = nameregex.sub(r'\1****',ac)
            for ad in ab :
                ad = re.sub(ac,ab,a)
            return ad
        
        elif abs_word_count == 2 :
            abs1 = [abs_word[0]]
            abs2 = [abs_word[1]]
    
            for ac in abs1 :
                nameregex = re.compile(r'(\w)\w*')
                ab = nameregex.sub(r'\1****',ac)
            for ad in ab :
                ad = re.sub(ac,ab,a)
            for ae in abs2 :
                nameregex = re.compile(r'(\w)\w*')
                af = nameregex.sub(r'\1****',ae)
            for ag in af :
                ag = re.sub(ae,af,ad)
            return ag
        
        elif abs_word_count == 3 :
            abs1 = [abs_word[0]]
            abs2 = [abs_word[1]]
            abs3 = [abs_word[2]]
    
            for ac in abs1 :
                nameregex = re.compile(r'(\w)\w*')
                ab = nameregex.sub(r'\1****',ac)
            for ad in ab :
                ad = re.sub(ac,ab,a)
    
            for ae in abs2 :
                nameregex = re.compile(r'(\w)\w*')
                af = nameregex.sub(r'\1****',ae)        
            for ag in af :
                ag = re.sub(ae,af,ad)
    
            for ah in abs3 :
                nameregex = re.compile(r'(\w)\w*')
                ai = nameregex.sub(r'\1****',ah)
            for aj in ai :
                ak = re.sub(ah,ai,ag)    
            return ak
        
        elif abs_word_count == 4 :
            abs1 = [abs_word[0]]
            abs2 = [abs_word[1]]
            abs3 = [abs_word[2]]
            abs4 = [abs_word[3]]

            for ac in abs1 :
                nameregex = re.compile(r'(\w)\w*')
                ab = nameregex.sub(r'\1****',ac)
            for ad in ab :
                ad = re.sub(ac,ab,a)

            for ae in abs2 :
                nameregex = re.compile(r'(\w)\w*')
                af = nameregex.sub(r'\1****',ae)
            for ag in af :
                ag = re.sub(ae,af,ad)
    
            for ah in abs3 :
                nameregex = re.compile(r'(\w)\w*')
                ai = nameregex.sub(r'\1****',ah)
            for aj in ai :
                ak = re.sub(ah,ai,ag)  
    
            for al in abs4 :
                nameregex = re.compile(r'(\w)\w*')
                am = nameregex.sub(r'\1****',al)
            for an in am :
                ao = re.sub(al,am,ak)
            return ao
        
        elif abs_word_count > 4 :
            ap = 'kalimat terlalu abusive'
            return ap
    
        else :
            textOK
            
        return str(a)
    
    text_clean = text_sensor(textOK)
          
    query_text ="update data set old_text =?, new_text=? where id=?" 
    val =(text, text_clean, id)
    mycursor.execute(query_text, val)
    data_base.commit()
    return "Data sukses diupdate"

@app.route("/data/csv", methods=["POST"])
def input_csv():
  if request.method == 'POST':
    file = request.files['file']
    data = pd.read_csv(file, encoding='iso-8859-1')
    listdata = data.iloc[:,0]
    text = listdata.to_list()
    
    def run(ab) :
        df = pd.read_csv(r'C:\Users\User\Documents\binar\Python\binar-academy\hint\filter_data.csv')
        filtertext = df.abusive.to_list()
        filter1 = re.sub('([^\x00-\x7f])|(USER)|(@[A-Za-z0-9_]+)|(#[A-Za-z0-9_]+)|(RT)','',ab)
        filter2 = re.sub(r'([^\w\s])|(\n)',' ',filter1)
        filter3 = re.sub('&amp;','dan',filter2)
        filter4 = re.sub(' +',' ',filter3)
        filter5 = filter4.lower()
        textOK = filter5.strip()
    
        word_split = textOK.split()
        abs_word = ([word for word in textOK.split() if word in filtertext])
        abs_word_count = len(abs_word)
        
        def text_sensor(a):
            if abs_word_count == 1 :
                abs1 = [abs_word[0]]
                for ac in abs1 :
                    nameregex = re.compile(r'(\w)\w*')
                    ab = nameregex.sub(r'\1****',ac)
                for ad in ab :
                    ad = re.sub(ac,ab,a)
                return ad
        
            elif abs_word_count == 2 :
                abs1 = [abs_word[0]]
                abs2 = [abs_word[1]]
    
                for ac in abs1 :
                    nameregex = re.compile(r'(\w)\w*')
                    ab = nameregex.sub(r'\1****',ac)
                for ad in ab :
                    ad = re.sub(ac,ab,a)
                for ae in abs2 :
                    nameregex = re.compile(r'(\w)\w*')
                    af = nameregex.sub(r'\1****',ae)
                for ag in af :
                    ag = re.sub(ae,af,ad)
                return ag
        
            elif abs_word_count == 3 :
                abs1 = [abs_word[0]]
                abs2 = [abs_word[1]]
                abs3 = [abs_word[2]]
    
                for ac in abs1 :
                    nameregex = re.compile(r'(\w)\w*')
                    ab = nameregex.sub(r'\1****',ac)
                for ad in ab :
                    ad = re.sub(ac,ab,a)
    
                for ae in abs2 :
                    nameregex = re.compile(r'(\w)\w*')
                    af = nameregex.sub(r'\1****',ae)        
                for ag in af :
                    ag = re.sub(ae,af,ad)
    
                for ah in abs3 :
                    nameregex = re.compile(r'(\w)\w*')
                    ai = nameregex.sub(r'\1****',ah)
                for aj in ai :
                    ak = re.sub(ah,ai,ag)    
                return ak
        
            elif abs_word_count == 4 :
                abs1 = [abs_word[0]]
                abs2 = [abs_word[1]]
                abs3 = [abs_word[2]]
                abs4 = [abs_word[3]]

                for ac in abs1 :
                    nameregex = re.compile(r'(\w)\w*')
                    ab = nameregex.sub(r'\1****',ac)
                for ad in ab :
                    ad = re.sub(ac,ab,a)

                for ae in abs2 :
                    nameregex = re.compile(r'(\w)\w*')
                    af = nameregex.sub(r'\1****',ae)
                for ag in af :
                    ag = re.sub(ae,af,ad)
    
                for ah in abs3 :
                    nameregex = re.compile(r'(\w)\w*')
                    ai = nameregex.sub(r'\1****',ah)
                for aj in ai :
                    ak = re.sub(ah,ai,ag)  
    
                for al in abs4 :
                    nameregex = re.compile(r'(\w)\w*')
                    am = nameregex.sub(r'\1****',al)
                for an in am :
                    ao = re.sub(al,am,ak)
                return ao
        
            elif abs_word_count > 4 :
                ap = 'kalimat terlalu abusive'
                return ap
    
            else :
                textOK
            
            return str(a)        
        
        text_clean = text_sensor(textOK)
        
        return str(text_clean)
    
    
    
    query_text = "insert into data(old_text,new_text) values(?,?)"
    val = (text, text_clean)
    mycursor.execute(query_text, val)
    data_base.commit()
    print(text)
    print(text_clean)
    return "Sukses input data"
        

@app.errorhandler(400)
def handle_400_error(_error):
  "return sebuah http 400 error kepada client"
  return make_response(jsonify({'error':'Misunderstood'}), 400)

@app.errorhandler(401)
def handle_401_error(_error):
   "return sebuah http 401 error kepada client"
   return make_response(jsonify({'error':'Unauthorised'}), 401)

@app.errorhandler(404)
def handle_404_error(_error):
   "return sebuah http 404 error kepada client"
   return make_response(jsonify({'error':'Not Found'}), 404)

@app.errorhandler(500)
def handle_500_error(_error):
   "return sebuah http 500 error kepada client"
   return make_response(jsonify({'error':'Server error'}), 500)  


if __name__ == '__main__':
  app.run(debug=True)


# In[ ]:




