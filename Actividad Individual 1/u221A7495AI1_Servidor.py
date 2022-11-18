import socket
import threading
import sys
import pickle
import os
import re as reg

class Servidor():

	def __init__(self, host=socket.gethostname(), port=int(input("Que puerto quiere usar ? "))):
		self.clientes = []
		self.nicknames = []
		print('\nSu IP actual es : ',socket.gethostbyname(host))
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(), '\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
		self.s = socket.socket()
		self.s.bind((str(host), int(port))) #Enlaza el puerto y el host
		self.s.listen(30)
		self.s.setblocking(False)

		threading.Thread(target=self.aceptarC, daemon=True).start()
		threading.Thread(target=self.procesarC, daemon=True).start()

		while True:
			msg = input('\n << SALIR = 1 >> \n') #Cierra el programa cuando se presiona el 1
			if msg == '1':
				print(" **** Me piro vampiro; cierro socket y mato SERVER con PID = ", os.getpid())
				self.s.close()
				sys.exit()
			else: pass

	def aceptarC(self):
		print('\nHilo ACEPTAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		
		while True:
			try:
				conn, addr = self.s.accept()
				print(f"\nConexion aceptada via {addr}\n")
				conn.setblocking(False)
				self.clientes.append(conn)
			except: pass

	def procesarC(self):
		print('\nHilo PROCESAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		while True:
			if len(self.clientes) > 0: 
				for c in self.clientes:
					try:
						data = c.recv(64) #Si encuentra a varios clientes se realiza el broadcast; caso contrario, no
						if data: self.broadcast(data,c)
					except: pass

	def broadcast(self, msg, cliente):
		mensaje=pickle.loads(msg)
		us=reg.search('^[^ :]*',mensaje)
		if us.group() not in self.nicknames:
			self.nicknames.append(us.group())
		for c in self.clientes: #Recorre y muestra cuántos clientes hay conectados
			print("Clientes conectados Right now = ", len(self.clientes))
			print("NICKNAMES")
			print(self.nicknames)
			for n in self.nicknames: #Recorre y muestra el nickname puesto por cada cliente
				print(n)			
			try:
				if c != cliente: 
					print(pickle.loads(msg)) #Recibe como parámetro el mensaje y devuelve el objeto deserializado.
					c.send(msg)
			except: self.clientes.remove(c)

arrancar = Servidor() 