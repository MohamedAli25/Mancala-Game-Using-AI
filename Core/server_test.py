import Network
import threading

serv= Network.Server()

serv.start()


while (True) :
    input()
    print(serv.messages)
    
 #   l =serv.get_conn_clients()
 #   print (l)
 #   try :
  #      serv.send(l[0] , 'helloo')
  #  except : 
  #      print ("list is empty")