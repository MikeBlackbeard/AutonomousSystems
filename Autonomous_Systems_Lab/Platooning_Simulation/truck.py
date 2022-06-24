import socket
import threading

FORMAT = 'utf-8'

HOST = "192.168.56.1"
PORT = 50505

t_role = 'string'

# Choosing TruckName
TruckName = input("Truck name: ")
Distance_Covered = input("Distance covered: ")
Match_of_Route = input("Match of route ( 0 for False and 1 for True): ")
Fuel_Consumption = input("Fuel Consumption: ")
Body_Characteristics = input("Body Characteristics (1 = bad, 2 = good, 3 = better, 4 = best): ")
Equipment_Sensors = input("Equipement sensors: ")
Efficiency = input("Efficiency (1 = bad, 2 = good, 3 = better, 4 = best): ")

TruckSpeed = input("Truck Speed: ")
TruckAngle = '0'

# Connecting To Server
truck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
truck.connect((HOST, PORT))

# Listening to Server and Sending TruckName
def receive():
    while True:
        try:
            # Receive Message From Server
            global TruckSpeed
            global TruckAngle
            message = truck.recv(1024).decode(FORMAT)
            if message == 'TRUCK_NAME':
                truck.send(TruckName.encode(FORMAT))

            elif message == 'DISTANCE':
                truck.send(Distance_Covered.encode(FORMAT))

            elif message == 'MATCH':
                truck.send(Match_of_Route.encode(FORMAT))

            elif message == 'FUEL':
                truck.send(Fuel_Consumption.encode(FORMAT))
            
            elif message == 'BODY':
                truck.send(Body_Characteristics.encode(FORMAT))
            
            elif message == 'SENSORS':
                truck.send(Equipment_Sensors.encode(FORMAT))

            elif message == 'EFF':
                truck.send(Efficiency.encode(FORMAT))

            elif message == 'MASTER_TRUCK' or message == 'SLAVE_TRUCK':
                global t_role 
                t_role = message
                print(f"assigned roll {t_role}")

            elif message == 'W_SPEED':
                truck.send(TruckSpeed.encode(FORMAT))

            elif 'C_SPEED' in message:
                temp = message.removeprefix('C_SPEED ')
                TruckSpeed = temp
                print(f'New speed: {TruckSpeed}')
                truck.send(''.encode(FORMAT))       

            elif 'C_ANGLE' in message:
                temp = message.removeprefix('C_ANGLE ')
                TruckAngle = temp
                print(f'New steering angle: {TruckAngle}')
                truck.send(''.encode(FORMAT))     

            else:
                print(message)
        except:
            # Close Connection When Error
            print("The platooning system has failed! Ending connection")
            print('Press any key to close')
            truck.close()
            break

# Sending Messages To Server
def write():
    while True:
        try:
            global TruckSpeed
            global TruckAngle
            global t_role
            msg = input()
            if msg == 'SPEED':
                print(f'Current speed: {TruckSpeed}')
            elif msg == 'ROLE':
                print(t_role)
            elif msg == 'ANGLE':
                print(f'Current angle: {TruckAngle}')
            elif 'C_ANGLE' in msg or 'C_SPEED' in msg:
                if t_role == 'MASTER_TRUCK':
                    truck.send(msg.encode(FORMAT))
                else:
                    print('Action only valid for Master Truck')
            else:
                message = '{}: {}'.format(TruckName, msg)
                truck.send(message.encode(FORMAT))
        except:
            truck.close()
            break

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()