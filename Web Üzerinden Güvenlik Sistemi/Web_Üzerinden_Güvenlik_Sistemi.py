import time
import datetime
import RPi.GPIO as GPIO
import sqlite3
from pad4pi import rpi_gpio
import sys


con = sqlite3.connect("zaman1.db")
kursor = con.cursor()                                  
kursor.execute("CREATE TABLE IF NOT EXISTS hareket (zaman TEXT,tarih TEXT)") 

algılanma_ = "Hareket Algılandı"
sifre = ""


def SifreAl(key):
  global sifre
  sifre += key
  print(key)
  
  if(sifre =="*5206#"):
    sifre = ""
    print("Giriş Başarılı...")
    print("Kilit Açılıyor...")
    print("Alarm Sistemleri Devre Dışı...")
    GPIO.output(24,True)
    time.sleep(1)
    GPIO.output(24,False)
    

  

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(26,GPIO.IN)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(5,GPIO.IN)

GPIO.output(24,False)
GPIO.output(20,False)

#Setup Keypad
KEYPAD = [
        ["1","2","3","A"],
        ["4","5","6","B"],
        ["7","8","9","C"],
        ["*","0","#","D"]
]
#same as calling: factory.create_4_by_4_keypad, still we put here fyi:
ROW_PINS = [4, 14, 15, 17] # BCM numbering; 
COL_PINS = [18, 27, 22, 23] # BCM numbering; 

#printKey will be called each time a keypad button is pressed
#şifre girme anahtarı aktif ise sunucunun başındaki kişi python kodunu yeniden başlatıcak ve şifre girişine izin verilecek.
#şifre doğru ise kapı kilidinin açıldığını ve kişinin bölüme girdiğini varsaymaktayız. Şifreyi doğru girerek içeri giren kişi
#için algılama ve alarm sistemlerinin hepsi devre dışı kalmaktadır.
if GPIO.input(26) == True:  
  factory = rpi_gpio.KeypadFactory()
  keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
  keypad.registerKeyPressHandler(SifreAl)


while True:
  
  
  try:
    if GPIO.input(26) == True :
      print("Birisi Şifre girmek için anahtarı aktif etti.")
      time.sleep(2)
      continue
    
    if GPIO.input(5) == True:
      GPIO.output(20,True)
      GPIO.output(24,True)
      time.sleep(1)
      GPIO.output(20,False)
      GPIO.output(24,False)

      zaman = time.time()
      tarih = str(datetime.datetime.fromtimestamp(zaman).strftime('%Y-%m-%d %H:%M:%S'))
      
      
      con = sqlite3.connect("zaman1.db")
      kursor = con.cursor()                            
                                                
      kursor.execute("INSERT INTO hareket (zaman,tarih) VALUES(?,?)",(algılanma_,tarih))
      con.commit()
        
      kursor.execute("SELECT * FROM hareket")
      zaman_verisi = kursor.fetchall()
      for each in zaman_verisi:
          print(each)
      con.close()
     
        
    
  except KeyboardInterrupt:
    
    
    keypad.cleanup()
    GPIO.cleanup()

    
