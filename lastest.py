
#Import library Regex, SQLite3, Pandas
import re
import pandas as pd
import sqlite3

#Import library Flask
from flask import Flask, jsonify
from flask import request, make_response
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

#Define deskripsi dari Swagger UI
app = Flask(__name__)
app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
    'title' : LazyString(lambda: 'API Documentation for Text Cleansing Abusive Word'),
    'version' : LazyString(lambda: 'version 1.0'),
    'description' : LazyString(lambda:'API Documentation for Text Abusive Cleansing'),
},
    host = LazyString(lambda: request.host)
)

swagger_config = {
    'headers' : [],
    'specs':[
        {
            'endpoint':'docs',
            'route':'/docs.json',
        }
    ],
    'static_url_path':'/flasgger_static',
    'swagger_ui': True,
    'specs_route':'/docs/'
}

swagger = Swagger(app,template=swagger_template,
                  config=swagger_config)

#Connect ke database
conn = sqlite3.connect('data/contoh.db', check_same_thread=False)

#Menyimpan data hasil text sebelum dan sesudah di-cleansing
conn.execute('''CREATE TABLE IF NOT EXISTS data (
text varchar(255),
text_clean varchar(255));
''')

#Define endpoint, data from user input
@swag_from("docs/upload_file.yml", methods=['POST'])
@app.route('/contoh_text',methods=['POST'])

def text_prepocessing():
    
    #user input
    file = request.files['file']
    data = pd.read_csv(file, encoding='iso-8859-1')
    listdata = data.iloc[:,0]
    text = listdata.to_list()
    
    #Regex untuk melakukan cleansing text
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

            
    #Memasukkan hasil cleasing ke dalam table
    conn.execute('''INSERT INTO data(text, text_clean) VALUES ('"+ text +"', '"+ text_clean +"')''')
    conn.commit()
    
    json_response = {
        'status_code' : 200,
        'description' : 'Abusive word have been successfully removed',
        'data' : text_clean,
    }
    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
    app.run()





