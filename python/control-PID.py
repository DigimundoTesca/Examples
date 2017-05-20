from datetime import datetime, timedelta

"""
Controlador PID

TODO: Obtener el Control Proporcional, Integral y Derivativo

La fórmula está dada por:
	( (K1 * (Sp + Mp + Ap) ) + (K2 * ( Sum(Ts) - Sum(Tp) ) / Dr) + Dp ) / 3 

En donde
	K1 = Constante Proporcional
	K2 =  Constante Integral
	K3 = Constante Derivativa
	Sp = Promedio por día de la Semana
	Mp = Promedio por dia del Mes
	Ap = Promedio por día del Año
	Ts = Suma del total de elementos en los días de la semana
	Tp = Suma del total de elementos promedios en todas las semanas registradas
	Dr = Días restantes -> 7 - Ts
	Dp = Promedio derivativo ( Mínimos cuadrados )
	
	*** K1, K2, K3 Son constantes que se van ajustando manualmente al final de la
	predicción inicial, de acuerdo a los valores reales obtenidos ***
"""


def main():
	"""
	Esta funcion su unico proposito será generar los cálculos pertinentes, además
	de que aquí configuraremos las constantes de control
	
	Inicialmente, K1 = k2 = k3 = 1
	
	Mientras se vayan obteniendo los resultados y se comparen con los valores reales, entonces
	se hacen los ajustes pertinentes a las constantes.
	
	Ejemplo:
		obtuvimos los siguientes valores para cada control:
		get_control_proporcional() = 5
		get_control_integral() =  7
		get_control_derivativo() = 13
		
		
		Pero el valor real para el día siguiente de la gelatina fue de 7
		por lo tanto se hace un ajuste a la primer constante k1, para que 
		5 * k1 nos de un valor aproximado a 7
		los mismo para las siguientes constantes
		de manera que:
		
			k1 * 5  = 7; 	k1 > 1
			k2 * 7  = 1; 	k2 = 1 ... aquí se mantuvo :D
			k3 * 13 = 13; 	k3 < 1 
			
			Ejemplo:
			De k3 ...
			si k3 > 1 entonces:
				k3 > 13 ... por lo tanto k3 * 13 > 7... y eso no nos sirve, ya que
				la venta real fue de 7, entonces nos estaríamos alejando más...
				la idea es realizarle ajustes a la constante para que el valor se acerque a 7 :D
	"""
	k1 = 1
	k2 = 1
	k3 = 1
	
	# Debemos enviarle un dato, el cual es el día que queremos calcular la predicción ...
	# Imaginando que hoy es DOMINGO 21 de mayo, por lo tanto enviamos el día a predecir
	# Es decir el Lunes 22 de mayo
	
	day_to_predict = datetime.today() + timedelta(days=1)  
	control_p = get_control_proporcional(day_to_predict)  
		

def get_control_proporcional(day_to_predict:datetime, :object):
	"""
	Este metodo nos retornará un PROMEDIO, pero qué promedios???
	
	1. Por DÍA [Lunes, Martes, Miercoles...]
	2. Por Número de día de cada MES [1, 2, 3, 4... 30, 31] 
	3. Por día del AÑO [1, 2, 3, 4, 5, ... 363, 364, 365]
	
	La Suma de estos tres valores nos indicarán el Control Proporcional
	
	Ejemplo:
		Hoy estamos a Lunes 15 de Mayo de 2017
		Sp
		Espera... me surgió una duda ...
		no recuerdo si aquí debería ser el promedio de TODOS los días que hay registro o
		el promedio de ventas de TODOS los lunes de los que se tiene registro ...
		
		Mp
		Calcular el promedio de todos los días 15 de TODOS los meses, por ejemplo 15 de enero, 
		15 de febrero, 15 de marzo... etc

		Ap 
		Calcular el promedio de ventas de todos los días X de todos los años 
		enero tiene 31...
		febero... 28 ? :v
		marzo 31...
		abril .. 30
		mayo ... -> 15
		
		por lo tanto, 31 + 28 + 31 + 30 +15 = 135 -> Mayo es el día 135 del año
		Ap sería el promedio de todos los días 135 de todos los años que se tenga registro
	"""
	
	#  Primero debemos hacer las consultas pertinentes :3
	
	#  Todas las siguientes deberías ser funciones, pero por ahora nel, todo aká :v 
	# Aquí debe estar la lógica para obtener la variable Sp
	# Hay que filtrar sólo los que tengan como fecha de creación un lunes :D
	
	"""
	En esta parte nos auxiliaremos de isoweekday que nos proveé python... 
	https://docs.python.org/3/library/datetime.html#datetime.date.isoweekday
	
	nos retornará un numero del 1 al 7 dependiendo de cada día
	siendo 1 lunes y 7 domingo
	así que una vez obtenidos todos los tickets, iteraremos su fecha de creacion
	y validaremos uno a uno los que cumplan a condicion requerida...
	
	Recordar: ya tenemos un método en helpers que nos retorna el numero de un día,
	pero nos retorna numero del 0 al 6, siendo lunes el 0 y 6 domingo
	"""
	from helpers import Helper()
	
	"""  Le tenemos que enviar el día del cual queremos obtener el numero
	correspondiente para hacer las validaciones """
	number_day = helper.get_number_day(day_topredict) + 1 # Este metodo ya incorpora isoweekday
	#  Como day_to_predict es Lunes 22 de mayo, nos retornará un 0, así que le sumamos uno, para que tenga sentido
	
	all_tickets_details = TicketDetail.objects.select_related('ticket').all()
	tickets_details_list = []
	total_days_dict = {}
	#  Ahora sí, vamos a iterar los tickets y a cada uno igual hay que convertir su atributo a entero
	
	for ticket_detail in all_tickets_details:
		if ticket_detail.ticket.created_at.isoweekday() == number_day:
			'Por lo tanto, ese ticket detail es de un día lunes :D'
			tickets_details_list.append(ticket_detail)
		""" Aquí obtendremos el total de lunes """
		total_days_dict[ticket_detail.ticket.created_at.strftime('%d-%m-%Y')] = True
		# Es obvio que si ya existe un ticket detail con la misma fecha no importa, ya que 
		# sólo indicaremos que si existen tickets en ese día ...
		
	
	""" ahora obtendremos el promedio de todos esos días, como son tickets details
	entonces ya incluye el producto vendido y obvio, el precio base y el total, pero necesitamos conocer el
	id de la gelatina, por lo tanto debemos pasarlo por argumento en la funcion
	en este caso pasaremos el objecto como tal...
	Una vez encontrado el ticket detail correspondiente podremos añadir las elementos que se 
	vendieron en ese movimiento
	"""
	
	total_elements = 0
	
	for ticket_detail in tickets_details_list:
		if ticket_detail.cartridge.id == product_object.id:
			'significa que es un ticket detail que vendio una gelatina'
			total_elements += ticket_detail.quantity
	
	#  Y listo, ahora total_elements nos indicará los elementos vendidos en todos los tiempos
	#  en los cuales haya sido una venta en un día lunes :3 -> Procedemos a promediar
	
	day_average = total_elements / len(total_days_dicts)  #  Promedio de dia = cantidad de elementos vendidos entre total de dias obtenidos
	
	""" Necesitamos calcular los días totales :D ¿Cómo los calcularias? 
	TIP: Te puedes guiar usando los tickets_details_list <- Contiene los datos que sí nos sirven
	
	TODO: Obtener la cantidad de lunes en TODOS los tiempos en los que se haya vendido la gelatina
	
	Solución:
		recordar que un diccionario tiene llaves irrepetibles, entonces podemos usar cada datetime como una llave
		por lo tanto iteramos todos los tickets details list ( que son los que ya están filtrados)
		y almacenamos cada llava y obviamente, cada que se encuentre otro ticket detail con la misma
		fecha (date, no confundir con datetime) entonces ya no será necesario crear otro espacio en el diccionario
		al final solo queda obtener el tamaño del diccionario y ya
	"""
	
	
	# Aquí debe estar la lógica para obtener la variable Mp
	
	# Aquí debe estar la lógica para obtener la variable Ap


def get_control_integral():
	"""
	Este método retornará la suma del total de ventas de un producto en un
	día 'n' de la semana menos el promedio de ventas en una semana del producto,
	dividido entre la diferencia de los días de la semana menos la cantidad
	de días evaluados.
		
		Ejemplo:
		en el día miercoles se han vendido 20 gelatinas, y sabemos que en promedio
		hasta la fecha de hoy, en una semana cualquiera el promedio es que se vendan 
		50 gelatinas, por lo tanto
		Ts = 20
		Tp = 50
		Dr = 7 - 3 = 4
		
	"""
	

def get_control_derivativo():
	"""
	Este método nos retornará la derivada del día anterior con respecto a su día anterior
	aquí es donde utilizaremos los mínimos cuadrados...
	hipoteticamente, imaginando que la semana pasada se vendieron en el siguiente 
	orden de días la cantidad de gelatinas:
		{'Lunes': 15, 
		'Martes': 5, 
		'Miércoles': 9: 
		'Jueves': 14, 
		'Viernes': 12, 
		'Sabado': 0, 
		'Domingo': 15
		}
	y al realizar las operaciones de los mínimos cuadrados obtuvimos las siguientes "Predicciones":
	(Hipoteticamente)
		{'Lunes': 13,
		'Martes': 7, 
		'Miércoles': 8: 
		'Jueves': 10, 
		'Viernes': 12, 
		'Sabado': 0, 
		'Domingo': 12
		}
	por lo tanto si hoy es lunes y queremos conocer las ventas de mañana martes utilizaríamos
	el valor correspondiente al martes: 7
	
	"""
	
	
if __name__ == '__main__':
	main()

