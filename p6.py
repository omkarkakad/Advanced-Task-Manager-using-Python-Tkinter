from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import Treeview, Style, Combobox
import sqlite3


#Main window
mw=Tk()
mw.geometry("760x700+300+50")
mw.title("🗂️ Advanced Task manager")
mw.configure(bg="beige")

#Defining commands

def view_task():
	mw.withdraw()
	vw.deiconify()
	for row in tree.get_children():
        	tree.delete(row)
	con=None
	try:
		con=sqlite3.connect("task_manager1.db")
		cursor=con.cursor()
		sql="select * from tasks"
		cursor.execute(sql)
		data=cursor.fetchall()
		for d in data:
			tree.insert("", END, iid=d[0], values=d[1:])

			

	except Exception as e:
		showerror("issue",e)
	finally:
		if con is not None:
			con.close()	


def back():
	vw.withdraw()
	mw.deiconify()
#Add the task
def add_task():
	con=None
	try:
		con=sqlite3.connect("task_manager1.db")
		cursor=con.cursor()
		cursor.execute('''create table if not exists tasks(id integer primary key autoincrement,title text not null,due_date text,priority text,status text)''')
		sql="INSERT INTO tasks (title, due_date, priority, status) VALUES (?, ?, ?, ?)"
		title=ent_title.get().strip()
		due=ent_due_date.get().strip()
		priority=ent_priority.get().strip()
		status=ent_status.get().strip()
		cursor.execute(sql,(title,due,priority,status))
		con.commit()
		showinfo("Success","Task Added Successfully")
		ent_title.delete(0, END)
		ent_due_date.delete(0, END)
		ent_priority.set("High")
		ent_status.set("Pending")			

	except Exception as e:
		showerror("issue",e)
	finally:
		if con is not None:
			con.close()
#Delete the task
def delete_task():
	con=None
	try:
		con=sqlite3.connect("task_manager1.db")
		cursor=con.cursor()
		sql="delete from tasks where id=?"
		selected = tree.selection()
		if not selected:
			showwarning("Delete Error", "No task selected.")
			return
		task_id = selected[0]
		cursor.execute(sql,(task_id,))
		con.commit()
		showinfo("Task Deleted","Selected Task is deleted Successfully")
		view_task()
			

	except Exception as e:
		showerror("issue",e)
	finally:
		if con is not None:
			con.close()
#update the task
def update_task():
    selected = tree.selection()
    if not selected:
        showwarning("Update Error", "No task selected.")
        return
    task_id = selected[0]
    con = sqlite3.connect("task_manager1.db")
    cur = con.cursor()
    cur.execute("UPDATE tasks SET title=?, due_date=?, priority=?, status=? WHERE id=?",
                (vw_ent_title.get(), vw_ent_due_date.get(), vw_ent_priority.get(), vw_ent_status.get(), task_id))
    con.commit()
    con.close()
    showinfo("Success","Task updated successfully")
    view_task()
    vw_ent_title.delete(0,END)
    vw_ent_due_date.delete(0,END)
    vw_ent_priority.set("High")
    vw_ent_status.set("Pending")

#Selecting the task
def on_task_select(event):
	selected=tree.selection()
	if not selected:
		return
	item=tree.item(selected[0])
	vals=item['values']


	vw_ent_title.delete(0, END)
	vw_ent_title.insert(0, vals[0])
	vw_ent_due_date.delete(0, END)
	vw_ent_due_date.insert(0, vals[1])
	vw_ent_priority.set(vals[2])
	vw_ent_status.set(vals[3])

def search_task():
    search_val = ent_task.get().lower()
    for row in tree.get_children():
        item = tree.item(row)['values']
        if any(search_val in str(v).lower() for v in item):
            tree.selection_set(row)
            tree.see(row)
            return
    showinfo("Search", "No matching task found.")






lab_mw=Label(mw,text="🗂️ Advanced Task Manager",font=("Arial",30,"bold"),bg="black",fg="beige")
lab_mw.pack(fill=X)

lab_title=Label(mw,text="Title/Task:",bg="beige",font=("Arial",30,"bold"))
lab_title.place(x=30,y=80)
ent_title=Entry(mw,font=("Arial",30,"bold"),width=20)
ent_title.place(x=270,y=80)

lab_due_date=Label(mw,text="Due Date:",bg="beige",font=("Arial",30,"bold"))
lab_due_date.place(x=30,y=180)
ent_due_date=Entry(mw,font=("Arial",30,"bold"),width=20)
ent_due_date.place(x=270,y=180)

lab_priority=Label(mw,text="Priority:",bg="beige",font=("Arial",30,"bold"))
lab_priority.place(x=30,y=280)
ent_priority=Combobox(mw,font=("Arial",30,"bold"), values=["High","Moderate","Low"],width=18,state="readonly")
ent_priority.place(x=270,y=280)
ent_priority.set("High")

lab_status=Label(mw,text="Status:",bg="beige",font=("Arial",30,"bold"))
lab_status.place(x=30,y=380)
ent_status=Combobox(mw,font=("Arial",30,"bold"), values=["Pending","In Progress","Completed"],width=18,state="readonly")
ent_status.place(x=270,y=380)
ent_status.set("Pending")

btn_add=Button(mw,text="Add Task",font=("Arial",25,"bold"),bg="green",fg="black",width=10,command=add_task)
btn_add.place(x=280,y=480)
btn_view_task=Button(mw,text="View Task",font=("Arial",25,"bold"),bg="purple",fg="black",width=10,command=view_task)
btn_view_task.place(x=280,y=580)

#View update delete task Window
vw=Toplevel(mw)
vw.geometry("1330x700+100+50")
vw.title("Advanced Task Manager")
vw.configure(bg="beige")

lab_searh=Label(vw,text="🔍 Search Task:",font=("Arial",20,"bold"),bg="beige")
lab_searh.place(x=20,y=20)
ent_task=Entry(vw,font=("Arial",20,"bold"),width=30)
ent_task.place(x=250,y=20)
btn_find=Button(vw,text="Find",font=("Arial",13,"bold"),bg="black",fg="beige",width=5,command=search_task)
btn_find.place(x=730,y=20)

vw_lab_title=Label(vw,text="Title/Task:",bg="beige",font=("Arial",20,"bold"))
vw_lab_title.place(x=20,y=100)
vw_ent_title=Entry(vw,font=("Arial",20,"bold"),width=20)
vw_ent_title.place(x=210,y=100)

vw_lab_due_date=Label(vw,text="Due Date:",bg="beige",font=("Arial",20,"bold"))
vw_lab_due_date.place(x=550,y=100)
vw_ent_due_date=Entry(vw,font=("Arial",20,"bold"),width=20)
vw_ent_due_date.place(x=700,y=100)

vw_lab_priority=Label(vw,text="Priority:",bg="beige",font=("Arial",20,"bold"))
vw_lab_priority.place(x=20,y=170)
vw_ent_priority=Combobox(vw,font=("Arial",20,"bold"), values=["High","Moderate","Low"],width=18,state="readonly")
vw_ent_priority.place(x=210,y=170)
vw_ent_priority.set("High")

vw_lab_status=Label(vw,text="Status:",bg="beige",font=("Arial",20,"bold"))
vw_lab_status.place(x=550,y=170)
vw_ent_status=Combobox(vw,font=("Arial",20,"bold"), values=["Pending","In Progress","Completed"],width=18,state="readonly")
vw_ent_status.place(x=700,y=170)
vw_ent_status.set("Pending")

#Display Task
display_frame = Frame(vw, bg="beige")
display_frame.place(x=0, y=220, width=1330, height=480)

style = Style()
style.configure("Treeview.Heading", font=("Arial", 18, "bold"), background="red", foreground="black")
style.configure("Treeview", font=("Arial", 15), background="black", foreground="white",rowheight=25)

tree = Treeview(display_frame, columns=("Title", "Due Date", "Priority", "Status"), show="headings")

tree.heading("Title", text="Title",anchor="w")
tree.heading("Due Date", text="Due Date",anchor="w")
tree.heading("Priority", text="Priority",anchor="w")
tree.heading("Status", text="Status",anchor="w")

tree.column("Title", width=250,anchor="w")
tree.column("Due Date", width=50,anchor="w")
tree.column("Priority", width=70,anchor="w")
tree.column("Status", width=80,anchor="w")
tree.bind("<Double-1>", on_task_select)
tree.pack(fill=BOTH, expand=True)

btn_update_task=Button(vw,text="Update",font=("Arial",18,"bold"),bg="orange",fg="black",width=8,command=update_task)
btn_update_task.place(x=820,y=20)
btn_delete_task=Button(vw,text="Delete",font=("Arial",18,"bold"),bg="red",fg="black",width=8,command=delete_task)
btn_delete_task.place(x=1000,y=20)
btn_back_task=Button(vw,text="Back",font=("Arial",18,"bold"),bg="black",fg="beige",width=8,command=back)
btn_back_task.place(x=1170,y=20)



vw.withdraw()



def on_closing():
	if askyesno("close","Sure You want to close Task Manager"):
		mw.destroy()
vw.protocol("WM_DELETE_WINDOW", on_closing)
mw.protocol("WM_DELETE_WINDOW", on_closing)
	

mw.mainloop()
