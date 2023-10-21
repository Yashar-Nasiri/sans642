##################################################################
# 1.This python script Extracts:                                 #
#     - all links in page                                        #
#     - all Javascript's variables in page                       #
#     - all json key/value pairs in page                         #
# 2. Sends a GET/POST request with previouslly found parameters. #
# 3. Checks Reflected Sent params in GET/POST response.          #
##################################################################
import requests,re,json,html,urllib3
from bs4 import BeautifulSoup as bs
url = 'https://domgo.at/cxss/example/3'
url = 'https://www.w3schools.com/js/js_json_syntax.asp'
url = 'https://shecan.ir/'

def print_links(links): 
    print('-'*35)
    print("Total Links in Page:")
    print("-"*35)
    i=0
    dname_start = url.find('://')
    dname_end = url.find('/',dname_start+3)
    domain_name = url[dname_start+3:dname_end]
    schema=url[0:dname_start]
    for link in links:
        i+=1
        print(f'link [{i}] = {schema}://{domain_name}{link}') 

def print_js_variables(js_variables_dict): # prints found js vars to the console
    print('-'*35)
    print('Total JavaScript Variables in Page:')
    print('-'*35)
    for item in js_variables_dict.items() :
        k,v=item
        print(f"{v} = {k}")

def print_jasons(json_dict):
    print('-'*35)
    print('Jsons Keys in Page:')
    print('-'*35)
    index=0
    for item in json_dict.items():
        key,val=item
        index+=1
        val=f"jsonParam_{index}"  # replace jason key/values with jparam_X values
        json_dict[key]=val
        print(f"{val} = {key}")
    
urllib3.disable_warnings()
try:
    res=requests.get(url,verify=False)
except:
    print("Bad URL")
    exit()

soup=bs(res.content,'html.parser')
links=[]
for anchor in soup.find_all('a', href=True):
    links.append(anchor['href'])
print_links(links)    

pattern_jsvars=r'var\s+([a-zA-Z0-9_]+)\s+=.*;'
js_var_names_as_tuple = re.findall(pattern_jsvars, res.content.decode("utf-8"), re.M,)
js_variables_dict={}
index=0
for js_var_tuple in js_var_names_as_tuple:
    index+=1
    js_variables_dict[js_var_tuple]=f'jsParam_{index}'
print_js_variables(js_variables_dict)

pattern_jsondata='{.*}'
json_like_texts = re.findall(pattern_jsondata, res.text, re.M)
json_dict={}
for json_text in json_like_texts:
    html_decoded = html.unescape(json_text)
    try:
        json_dict.update(json.loads( html_decoded ))
    except :
       pass
print_jasons(json_dict)
      
 
# 4.Gains "A" Point for Mr. Sharifzade's Student ;)    
