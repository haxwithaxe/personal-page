#!/usr/bin/python
## Cookie Auth Script
import xml.dom.minidom, string, cgi, os, re, feedparser, datetime, cgitb
cgitb.enable()

KEY = '0' # Output of cmdline pi 42
DEMO_SWITCH = 'demo'
START_SWITCH = '0'
WORK_SWITCH = '1'
START_TEMPLATE = open("start.tmpl", "r")
TMPL = START_TEMPLATE.read()

MONO_TEMPLATE = open("mono.tmpl", "r")
MONO_TMPL = MONO_TEMPLATE.read()

welcomRedir = '<html><head><meta http-equiv="refresh" content="0;url=welcome.py"></head><body>&nbsp;</body></html>'

rssFrameStr = '<td align="left" valign="top"><h5>RSS</h5><div id="allrssdiv" class="frame">&nbsp;</div></td>'

addForm = '<div class="add-todoitem"><form method="POST" atcion="%url%">'
addForm += '<span id="objective"><input type="textbox" name="objective" size="40"/></span>'
addForm += '<span id="status"><input type="checkbox" name="status" unchecked/></span>'
addForm += '<span id="priority"><select name="priority"><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option><option>6</option><option>7</option><option>8</option><option>9</option><option selected>0</option></select></td>'
addForm += '<span id="action"><input type="submit" name="action" value="add"/></span>'
addForm += '</form></div>'

INNOVE_RSS = '<div id="innove-feed-control" style="color:#FFFFFF;font-size:14px;font-color:#000000;margin:10px;padding:4px;"><span style="color:#676767;font-size:14px;font-color:#000000;margin:10px;padding:4px;">Loading...</span></div>'
SEC_RSS = '<div id="sec-feed-control"><span style="color:#676767;font-size:14px;font-color:#000000;margin:10px;padding:4px;">Loading...</span></div>'
DEMO_RSS = SEC_RSS

NOAUTH_STR = '<html><body><h1>It Works!</h1></body></html>'
AUTH_STR = '<html><head><title>Redirecting...</title><meta http-equiv="REFRESH" content="5;url=start.py?uchi='+KEY+'&sore='+START_SWITCH+'"/></head><body><h1>It Still Works!</h1></body></html>'

LINKS = [{'url':'http://www.revision3.com','name':'Revision3'},{'url':'http://docs.python.org/','name':'Python Docs'}]
DEMO_LINKS = [{'url':'http://innovetech.com/','name':'Innove Technologies'},{'url':'http://www.fivestarwifi.com/','name':'Five Star WiFi'},{'url':'http://www.revision3.com','name':'Revision3'},{'url':'http://docs.python.org/','name':'Python Docs'}]

STYLE = 'koepkes-style.css'
DEMO_STYLE = STYLE
WORKLINKS = [{'url':'https://tanuj.is-very-evil.org:7201/','name':'Twiki'},{'url':'http://tanuj.is-very-evil.org:7032/','name':'Trac'},{'url':'http://5starwifi.com/charts/chartlist.html','name':'ShopFront Usage Charts'}]
# {'url':'','name':''}

TODO_XML = "todo.xml" # path to todo.xml where todos are kept
DEMO_TODO = 'demo-todo.xml' # path to demo todo xml so my personal ones don't get fubar'd
REMINDER_XML = 'reminderFinder.py' # there will be a script that pulls data from a exchange type server and outputs xml
args = cgi.parse()

def get_doc(file):
   return xml.dom.minidom.parse(file)

def get_url(vals):
   url = os.environ.get('SCRIPT_NAME', '')+'?uchi='+str(vals['uchi'] or 'demo')+'&sore='+str(vals['sore'] or 0)+'&koko='+str(vals['koko'] or 'main')
   return str(url)

def var_file(File):
   fo = open(File,'r')
   return fo.read()

def showTodoForm(file,vals):
   url = get_url(vals)
   add_form = addForm.replace('%url%',url)
   try:
      doc = xml.dom.minidom.parse(file)
   except:
      return '<span class="section">ToDos</span><div id="todolist">'+add_form+'</div>'
   root_node = doc.childNodes[0]
   output = '<div id="todolist">'
   for i in root_node.childNodes:
      try:
         if i.getAttribute('status') == '0':
            output += '<div class="todoitem"><form method="POST" atcion="'+url+'"><input type="hidden" name="id" value="'+i.getAttribute('tdid')+'"/>'
            output += '<span id="objective"><input type="textbox" name="objective" size="'+str(len(i.getAttribute('objective')))+'" value="'+i.getAttribute('objective')+'"/></span>'
            output += '<span id="status"><input type="checkbox" name="status" value="1"/></span>'
            output += '<span id="priority"><select name="priority"><option selected>'+i.getAttribute('priority')+'</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option><option>6</option><option>7</option><option>8</option><option>9</option><option>0</option></select></span>'
            output += '<span id="action"><input type="submit" name="action" value="modify"/><input type="submit" name="action" value="delete"/></span>'
            output += '</form></div>'
      except:
         continue
   for i in root_node.childNodes:
      try:
         if i.getAttribute('status') == '1':
            output += '<div class="todoitem-done"><form method="POST" atcion="'+url+'"><input type="hidden" name="id" value="'+i.getAttribute('tdid')+'"/>'
            output += '<span id="objective"><input type="hidden" name="objective" value="'+i.getAttribute('objective')+'"/>'+i.getAttribute('objective')+'</span>'
            output += '<span id="status"><input type="checkbox" name="status" value="1" checked/></span>'
            output += '<span id="priority"><input type="hidden" name="priority" value="'+i.getAttribute('priority')+'"/>'+i.getAttribute('priority')+'</span>'
            output += '<span id="action"><input type="submit" name="action" value="modify"/><input type="submit" name="action" value="delete"/></span>'
            output += '</form></div>'
      except:
         continue
   output += add_form
   output += '</div>'
   return output

def showTodos(file,vals):
   todore = re.compile('koko\=[a-z,A-Z]*')
   url = todore.sub('koko=todo',get_url(vals))
   add_form = addForm.replace('%url%',url)
   try:
      doc = xml.dom.minidom.parse(file)
   except:
      return '<div id="todolist">'+add_form+'</div>'
   root_node = doc.childNodes[0]
   output = '<div id="todolist">'
   for i in root_node.childNodes:
      try:
         if i.getAttribute('status') == '0':
            output += '<span class="not-done">'+i.getAttribute('objective')+' priority: '+str(i.getAttribute('priority'))+'</span><br/>'
      except:
         continue
   for i in root_node.childNodes:
      try:
         if i.getAttribute('status') == '1':
            output += '<span class="done">'+i.getAttribute('objective')+'</span><br/>'
      except:
         continue
   output += '<a target="ToDos" href="'+url+'">Modify ToDos</a></div>'
   return output

def write_doc_to_file(doc,file):
   todo_file = open(file,"w")
   doc.writexml(todo_file,encoding="utf-8")
   todo_file.close()

def find_todo(tdid,rootnode):
   element = False
   for i in rootnode.childNodes:
      try:
         if i.getAttribute("tdid") == tdid:
            element = i
            break
      except:
         continue
   return element

def get_new_tdid(doc):
   id = 0
   try:
      id = doc.childNodes[0].childNodes.length
   except:
      pass
   id += 1
   return str(id)

def add_todo(doc,rootnode,vals):
   tdid = get_new_tdid(doc)
   todo_element = doc.createElementNS(None,"todo")
   todo_element.setAttribute("objective",str(vals['objective']))
   todo_element.setAttribute("tdid",str(tdid))
   todo_element.setAttribute("user",str(vals['user']))
   todo_element.setAttribute("status",str(vals['status']))
   todo_element.setAttribute("priority",str(vals['priority']))
   rootnode.appendChild(todo_element)
   doc.appendChild(rootnode)
   return doc

def mod_todo(tdid,doc,rootnode,vals):
   todo_old = find_todo(tdid,rootnode)
   if todo_old:
      todo_new = doc.createElementNS(str(vals['objective']),"todo")
      todo_new.setAttribute("objective",str(vals['objective']))
      todo_new.setAttribute("tdid",str(vals['tdid']))
      todo_new.setAttribute("user",str(vals['user']))
      todo_new.setAttribute("status",str(vals['status']))
      todo_new.setAttribute("priority",str(vals['priority']))
      rootnode.replaceChild(todo_new,todo_old)
      doc.appendChild(rootnode)
   else:
      doc = add_todo(doc,rootnode,vals)
   return doc

def del_todo(tdid,doc,rootnode):
   todo_element = find_todo(tdid,rootnode)
   if todo_element:
      rootnode.removeChild(todo_element)
      doc.appendChild(rootnode)
   else:
      return doc
   return doc

def todo_main(args):
   try:
      tdid = args['id'][0]
   except:
      tdid = "0"

   try:
      priority = args['priority'][0]
   except:
      priority = "9"

   try:
      status = args['status'][0]
   except:
      status = "0"

   try:
      objective = args['objective'][0]
   except:
      objective = 'empty todo'

   try:
      user = args['user'][0]
   except:
      user = "0"

   try:
      action = args['action'][0]
   except:
      action = 'none'

   try:
      doc = get_doc(TODO_XML)
      rootnode = doc.childNodes[0]
   except:
      doc = xml.dom.minidom.Document()
      rootnode = doc.createElementNS(None,"todos")


   vals = {"user":user,"tdid":tdid,"objective":objective,"priority":priority,"status":status}
   if action == "add":
      doc = add_todo(doc,rootnode,vals)
      write_doc_to_file(doc,TODO_XML)
   if action == "modify":
      doc = mod_todo(tdid,doc,rootnode,vals)
      write_doc_to_file(doc,TODO_XML)
   if action == "delete":
      doc = del_todo(tdid,doc,rootnode)
      write_doc_to_file(doc,TODO_XML)

def links(links):
   output = ''
   for i in links:
      output += '<p><a target="_blank" href="'+i["url"]+'">'+i["name"]+'</a></p>'
   return output

def todo_form(xml,vals):
   return showTodoForm(xml,vals)

def todo(xml,vals):
   return showTodos(xml,vals)

def remind(xml):
   return ''

def dlstats():
   return ''

def style(css_file):
   CSS_DOC = open(css_file, "r")
   CSS = CSS_DOC.read()
   return CSS

def determineAuth():
   return KEY

def get_user_data(uid):
   userDataArray = {'uid':uid}
   if uid == DEMO_SWITCH:
      userDataArray['css'] = DEMO_STYLE
      userDataArray['feed'] = DEMO_RSS
      userDataArray['links'] = DEMO_LINKS
      userDataArray['todos'] = DEMO_TODO
   else:
      # xml reading here. faking xml data 'til it's there 
      css = "koepkes-style.css"
      feed = SEC_RSS
      links = LINKS
      todoxml = TODO_XML
      userDataArray['css'] = css
      userDataArray['feed'] = feed
      userDataArray['links'] = links
      userDataArray['todos'] = todoxml
   return userDataArray


def main():
   output = ''
   todo_main(args)
   urlVals = {}
   try:
      auth_stat = args['uchi'][0]
      urlVals['uchi'] = auth_stat
   except:
      auth_stat = None

   if auth_stat == KEY:
      isauth = True
      user = get_user_data(auth_stat)
   elif auth_stat == DEMO_SWITCH:
      isauth = True
      user = get_user_data(DEMO_SWITCH)
      #print(user)
   else:
      output = NOAUTH_STR.encode('utf-8')
      return output

   try:
      o_stat = args['sore'][0]
      urlVals['sore'] = o_stat
   except:
      o_stat = None

   try:
      koko_stat = args['koko'][0]
      urlVals['koko'] = koko_stat
   except:
      koko_stat = 'main'
      urlVals['koko'] = koko_stat


   START_STR = TMPL.replace('<!--style-->',style(user['css'])).replace('<!--links-->',links(user['links'])).replace('<!--todo-->',todo(user['todos'],urlVals)).replace('<!--reminders-->',remind(REMINDER_XML)).replace('<!--dl_stats-->',dlstats())

   WORK_STR = TMPL.replace('<!--style-->',style(user['css'])).replace('<!--links-->',links(WORKLINKS)).replace('<!--todo-->',todo(user['todos'],urlVals))

   TODO_STR = MONO_TMPL.replace('<!--style-->',style(user['css'])).replace('<!--todo-->',todo_form(user['todos'],urlVals))

   if str(o_stat) == WORK_SWITCH:
      where = 'work'
      if auth_stat == DEMO_SWITCH:
         where = 'demo'
   if str(o_stat) == START_SWITCH:
      where = 'start'
      if auth_stat == DEMO_SWITCH:
         where = 'demo'

   if koko_stat:
      if str(koko_stat) == 'todo' and isauth:
         output = TODO_STR
      if str(koko_stat) == 'main' and isauth:
         if where == 'start':
            output = START_STR
         if where == 'work':
            output = WORK_STR
   else:
      output = welcomeRedir

   output = output.encode('utf-8')
   return output

print 'Content-Type: text/html\n'
# print(cgi.parse())
print(main())
