#!/usr/bin/python
########################################################################
# Author: Chris Koepke
# Date: 2010/02/23
# Decription:
#  This script is used to write to the todo.xml file
########################################################################

import xml.dom.minidom,sys,cgi,cgitb
cgitb.enable()

TODO_XML = "todo.xml" # path to todo.xml where todos are kept
args = cgi.parse()

def get_doc(file):
   return xml.dom.minidom.parse(file)

def show_doc(file):
   addForm = '<tr class="add-todoitem"><td><form method="POST" atcion="'+str(sys.argv[0])+'"></td>'
   addForm += '<td id="objective"><input type="textbox" name="objective" size="40"/></td>'
   addForm += '<td id="status"><input type="checkbox" name="status" unchecked/></td>'
   addForm += '<td id="priority"><select name="priority"><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option><option>6</option><option>7</option><option>8</option><option>9</option><option selected>0</option></select></td>'
   addForm += '<td id="action"><input type="submit" name="action" value="add"/></td>'
   addForm += '</form></tr>'
   try:
      doc = xml.dom.minidom.parse(file)
   except:
      return '<table id="todolist">'+addForm+'</table>'
   root_node = doc.childNodes[0]
   output = '<table id="todolist">'
   for i in root_node.childNodes:
      try:
         if i.getAttribute('status') == '0':
            output += '<tr class="todoitem"><td><form method="POST" atcion="'+str(sys.argv[0])+'"><input type="hidden" name="id" value="'+i.getAttribute('tdid')+'"/></td>'
            output += '<td id="objective"><input type="textbox" name="objective" size="'+str(len(i.getAttribute('objective')))+'" value="'+i.getAttribute('objective')+'"/></td>'
            output += '<td id="status"><input type="checkbox" name="status" value="1"/></td>'
            output += '<td id="priority"><select name="priority"><option selected>'+i.getAttribute('priority')+'</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option><option>6</option><option>7</option><option>8</option><option>9</option><option>0</option></select></td>'
            output += '<td id="action"><input type="submit" name="action" value="modify"/><input type="submit" name="action" value="delete"/></td>'
            output += '</form></tr>'
      except:
         continue
   for i in root_node.childNodes:
      try:
         if i.getAttribute('status') == '1':
            output += '<tr class="todoitem-done"><td><form method="POST" atcion="'+str(sys.argv[0])+'"><input type="hidden" name="id" value="'+i.getAttribute('tdid')+'"/></td>'
            output += '<td id="objective"><input type="hidden" name="objective" value="'+i.getAttribute('objective')+'"/>'+i.getAttribute('objective')+'</td>'
            output += '<td id="status"><input type="checkbox" name="status" value="1" checked/></td>'
            output += '<td id="priority"><input type="hidden" name="priority" value="'+i.getAttribute('priority')+'"/>'+i.getAttribute('priority')+'</td>'
            output += '<td id="action"><input type="submit" name="action" value="modify"/><input type="submit" name="action" value="delete"/></td>'
            output += '</form></tr>'
      except:
         continue
   output += addForm
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

print('Content-type: text/html\n\n')
todo_main(args)
print(show_doc(TODO_XML))