from tkinter import *
from tkinter import messagebox
from datetime import datetime
import pytz
import requests

IST= pytz.timezone('Asia/Kolkata')

main= Tk()

main.geometry("920x690+200+0")
main.title(f" Near Vaccination Center")
'''main.iconbitmap()'''

main_color="#293241"
black_color='#292320'
main.config(background='#008B8B')
main.resizable(False,False)
photo = PhotoImage(file="top.png")
up_frame= Frame(main, height=120, width=700 ,bg="#5c4ce1",bd=1 ,relief=FLAT)
up_frame.place(x=0,y=0)
down_frame= Frame(main, height=30, width=920 ,bg='black',bd=1 ,relief=FLAT)
down_frame.place(x=0,y=230)
label = Label(up_frame, image = photo)
label.pack()
#pincode entry
pin_text = StringVar()
pincode = Entry(main, width=16, bg ="#eaf2ae", font = "verdana 12", textvariable= pin_text)
pincode.place(x=360,y=130)

date_format=StringVar()
date = Entry(main, width=16, bg ="#eaf2ae", font = "verdana 12", textvariable= date_format)
date.place(x=560,y=130)
date['textvariable']=date_format

pincode_image=PhotoImage(file="pincode.png")
l1=Label( image = pincode_image)
l1.place(x=410,y=25)

calendar_image=PhotoImage(file="calendar.png")
l1=Label( image = calendar_image)
l1.place(x=610,y=25)


label_pincode= Label(text="Pincode" , bg="#00FFFF", font='verdana 14')
label_pincode.place(x=395,y=90)

label_calendar= Label(text="Date[dd-mm-yyyy]" , bg="#00FFFF", font='verdana 12')
label_calendar.place(x=560,y=90)

searchbar=Label(text="Search\n Vaccine Center",bg="#00FFFF", font= 'verdana 12')
searchbar.place(x=740,y=170)

label_image=PhotoImage(file="clock.png")
label_clock= Label(image= label_image)
label_clock.place(x=135,y=75)

current_date= Label(text='currentdate',fg='black',font= 'verdana 17')
current_date.place(x=85,y=130)

current_time= Label(text='currentdate',fg='black',font= 'verdana 17')
current_time.place(x=85,y=160)




black_label = Label ( text =" Status          \tCenter - Name\t       Age-Group         Vaccine           Dose_1       Dose_2       Total", bg= "black", fg='white' , font= "verdana 11 bold")
black_label.place(x=0,y=233)



status_box= Text(main, height=29, width=11, bg='#008B8B',fg='#ecfcff',relief=FLAT, font="verdana 10")
status_box.place(x=3,y=260)

Centre_box= Text(main, height=29, width=36, bg='#008B8B',fg='#ecfcff',relief=FLAT, font="verdana 10")
Centre_box.place(x=100,y=260)

Age_group_box= Text(main, height=29, width=12, bg='#008B8B',fg='#ecfcff',relief=FLAT, font="verdana 10")
Age_group_box.place(x=400,y=260)

vaccine_box= Text(main, height=29, width=14, bg='#008B8B',fg='#ecfcff',relief=FLAT, font="verdana 10")
vaccine_box.place(x=510,y=260)

Dose_1_box= Text(main, height=29, width=12, bg='#008B8B',fg='#ecfcff',relief=FLAT, font="verdana 10")
Dose_1_box.place(x=630,y=260)

Dose_2_box= Text(main, height=29, width=12, bg='#008B8B',fg='#ecfcff',relief=FLAT, font="verdana 10")
Dose_2_box.place(x=735,y=260)

Total_box= Text(main, height=29, width=9, bg='#008B8B',fg='#ecfcff',relief=FLAT, font="verdana 10")
Total_box.place(x=840,y=260)

def Real_Time_clock():
    raw_Ts= datetime.now(IST)
    date_now= raw_Ts.strftime("%d %b %Y")
    time_now= raw_Ts.strftime("%H:%M: %S %p")
    current_date.config(text=date_now)
    current_time.config(text=time_now)
    current_time.after(1000, Real_Time_clock)
    
Real_Time_clock()



def insert_current_date():
    raw_TS= datetime.now(IST)
    format=raw_TS.strftime('%d-%m-%Y')
    date_format.set(format)

check_var= IntVar()
Today_date = Checkbutton(main, text='Today',bg="#00FFFF",width=0,variable=check_var, onvalue=1, offvalue=0, command=insert_current_date,font= 'verdana 10')
Today_date.place(x=560,y=160)

url= 'http://ipinfo.io/postal'
def get_pincode(url):
    response_pincode= requests.get(url).text
    return response_pincode

def fill_pincode():
    curr_pincode=get_pincode(url)
    pin_text.set(curr_pincode)


check_loc_var= StringVar()
current_location = Radiobutton(main, text='Current Location',bg="#00FFFF",width=0,variable=check_loc_var, value= check_loc_var, command=fill_pincode,font= 'verdana 10')
current_location.place(x=360,y=160)

def api_call(PINCODE, DATE):
    header={'user_agent': 'Chrome/84.0.4147.105 Safari/537.36'}
    request_Link= f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={PINCODE}&date={DATE}"
    response = requests.get(request_Link, headers=header)
    print(response)
    response_json=response.json()
    print(response_json)
    return response_json


def clear_content():
    status_box.delete('1.0',END)
    Centre_box.delete('1.0',END)
    vaccine_box.delete('1.0',END)
    Age_group_box.delete('1.0',END)
    Dose_1_box.delete('1.0',END)
    Dose_2_box.delete('1.0',END)
    Total_box.delete('1.0',END)

 
def search_vaccine_avl():
    clear_content()
    PINCODE =pin_text.get().strip()
    print(PINCODE)
    DATE= date_format.get()
    response_json= api_call(PINCODE,DATE)
   
    
    try:
        if len(response_json['sessions']) == 0 :
            messagebox.showinfo("INFO","Vaccine are not available for the given date")
        for sess in response_json['sessions']:
            age_limit     = sess['min_age_limit']
            centre_name   = sess['name']
            pincodes      = sess['pincode']
            vaccine_name  = sess['vaccine']   
            available_capc= sess['available_capacity']
            qty_d1        = sess['available_capacity_dose1']
            qty_d2        = sess['available_capacity_dose2']
            slot_date     = sess['date']
            
            
            if available_capc> 0:
                curr_status ='Available'
            else:
                curr_status='NA'
            
            if age_limit==45:
                age_group = '45+'
            else :
                age_group ='18-44'
                
            status_box.insert(END, f"{curr_status:^6s}")
            status_box.insert(END,"\n")
            Centre_box.insert(END, f"{centre_name:<30.29s}")
            Centre_box.insert(END,"\n")
            Age_group_box.insert(END, f"{age_group:^6s}")
            Age_group_box.insert(END,"\n")
            vaccine_box.insert(END, f"{vaccine_name:8s}")
            vaccine_box.insert(END,"\n")
            Dose_1_box.insert(END, f"{qty_d1:>5}")
            Dose_1_box.insert(END,"\n")
            Dose_2_box.insert(END, f"{qty_d2:>5}")
            Dose_2_box.insert(END,"\n")
            Total_box.insert(END, f"{available_capc:<5}")
            Total_box.insert(END,"\n")
            
    except KeyError as kt:
        messagebox.showerror("ERROR", "No Available centres for the given pincode and date")
        
search=PhotoImage(file="search.png")
search_center=Button(main, bg="#eaf2ae",relief= RAISED, command=search_vaccine_avl,image=search)
search_center.place(x=770,y=90)

            


main.mainloop()