from subprocess import check_output as run_script
from flask import Flask
from flask import render_template as render
from flask import url_for
from flask import redirect
from flask import request
from flask_cors import CORS as cors_for_flask
from os import access as check_exists
from os import F_OK as check_file
from os import remove as del_file
from os import mkdir as make_dir
from os import rmdir as remove_dir
from os import listdir
from os import chdir as cd

app = Flask(__name__, template_folder='src', static_folder='static')

floders={}

def del_symb(text):
    resu=text.replace('""','').replace('/','').replace('\\','')
    if resu=='':
        return False
    return resu;

@app.route('/')
def index():
    return render('index.html')

@app.route('/run_script/<string:line>/<string:encoding>')
def get_result(line,encoding):
    result=''
    result=str(run_script(line,shell=True,encoding=encoding))
    result=result.replace('\n','<br>')
    return result

@app.route('/create/<string:namer>/<string:password>')
def create(namer, password):
    try:
        make_dir(del_symb(namer))
        temp_f=open(namer+'\\password.txt','w')
        temp_f.write(password)
        temp_f.close()
    except:
        return "Errror :( . Maybe Project is Already exists?"
    return render('redirect.html',url='/')

@app.route('/edit/<string:namer>/<string:password>')
def editor(namer, password):
    try:
    #if True:
        temp_f=open(del_symb(namer)+'\\password.txt','r')
        readed=temp_f.read()
        temp_f.close()
        if str(password)==str(readed):
            dir=[]
            for i in listdir(del_symb(namer)):
                if not i=='password.txt':
                    dir.append(i)
            return render('edit.html',dir=dir)
        else:
            return "Password error :("
    except:
        return "Error :("

@app.route('/edit/<string:namer>/<string:password>/del/<string:file>')
def deleter_file_name(namer, password, file):
    try:
        temp_f=open(del_symb(namer)+'\\password.txt','r')
        readed=temp_f.read()
        temp_f.close()
        if str(password)==str(readed):
            try:
                del_file(del_symb(namer)+'\\'+file)
            except:
                return "Error!"
        else:
            return "Password error :("
    except:
        return "Error :("
    return render('redirect.html',url='/')

@app.route('/edit/<string:namer>/<string:password>/run/<string:file>/<string:encoding>')
def run_script_file_name(namer, password, file, encoding):
    try:
        temp_f=open(del_symb(namer)+'\\password.txt','r')
        readed=temp_f.read()
        temp_f.close()
        if str(password)==str(readed):
            try:
                tempf=open(del_symb(namer)+'\\'+file,'r')
                content=tempf.read()
                tempf.close()
                content=content.replace('fix_pynline_chdir','fix_pynline_chdir_idiots')
                if not content.split('\n')[0]=='from os import chdir as fix_pynline_chdir':
                    content='from os import chdir as fix_pynline_chdir\nfix_pynline_chdir("'+del_symb(namer)+'")\n'+content
                tempfail=open(del_symb(namer)+'\\'+file+'.tmp.py','w')
                tempfail.write(content)
                tempfail.close()
                try:
                    result=str(run_script('python '+str(del_symb(namer)+'\\'+file+'.tmp.py'),shell=True,encoding=str(encoding)))
                except:
                    return 'Errror while run'
                result=result
                temp_f=open(namer+'\\Log_'+str(file)+'.txt','w')
                temp_f.write(result)
                temp_f.close()
                return result.replace('\n','<br>')
            except:
                return "Error!"
        else:
            return "Password error :("
    except:
        return "Error :("
    return render('redirect.html',url='/')

@app.route('/edit/<string:namer>/<string:password>/create/<string:file>')
def create_file_name(namer, password, file):
    try:
    #if True:
        temp_f=open(del_symb(namer)+'\\password.txt','r')
        readed=temp_f.read()
        temp_f.close()
        if str(password)==str(readed):
            try:
            #if True:
                if not file=='password.txt':
                    tempf=open(del_symb(namer)+'\\'+file,'w')
                    resulter=tempf.write('print("Hello, world from python!")')
                    tempf.close()
            except:
                return "Error!"
        else:
            return "Password error :("
    except:
        return "Error :("
    return render('redirect.html',url='/')


@app.route('/edit/<string:namer>/<string:password>/edit/<string:file>')
def edit_file_name(namer, password, file):
    try:
        temp_f=open(del_symb(namer)+'\\password.txt','r')
        readed=temp_f.read()
        temp_f.close()
        if str(password)==str(readed):
            try:
                if not file=='password.txt':
                    tempf=open(del_symb(namer)+'\\'+file,'r')
                    resulter=tempf.read()
                    tempf.close()
                    return render('coder.html',lines=resulter)
            except:
                return "Error!"
        else:
            return "Password error :("
    except:
        return "Error :("
    return "error!"

@app.route('/edit/<string:namer>/<string:password>/edit/<string:file>/save/<string:lines>')
def edit_file_name_save(namer, password, file, lines):
    try:
        temp_f=open(del_symb(namer)+'\\password.txt','r')
        readed=temp_f.read()
        temp_f.close()
        if str(password)==str(readed):
            try:
                if not file=='password.txt':
                    tempf=open(del_symb(namer)+'\\'+file,'w')
                    tempf.write(lines.replace('-<br>-xdd','\n').replace('-<slash>-xdd','/').replace('-<backslash>-xdd','\\').replace('-<hashtag>-xdd','#'))
                    tempf.close()
                    return render('redirect.html',url='/')
            except:
                return "Error!"
        else:
            return "Password error :("
    except:
        return "Error :("
    return "error!"

@app.route('/delete/<string:namer>/<string:password>')
def deleter(namer, password):
    try:
        temp_f=open(del_symb(namer)+'\\password.txt','r')
        readed=temp_f.read()
        temp_f.close()
        if str(password)==str(readed):
            for i in listdir(del_symb(namer)):
                del_file(del_symb(namer)+'\\'+i)
            remove_dir(del_symb(namer))
        else:
            return "Password error :("
    except:
        return "Error :("
    return render('redirect.html',url='/')

@app.route('/edit/<string:namer>/<string:password>')
def load(namer, password):
    return render('redirect.html',url='/')

@app.errorhandler(404)
def page_not_found(e):
    return render('404.html',error=e), 404

if __name__=='__main__':
    app.run(debug=True)
