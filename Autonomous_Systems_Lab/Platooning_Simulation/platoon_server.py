import threading
import socket

from numpy import uintp

FORMAT = 'utf-8'

# Connection Data
host = socket.gethostbyname(socket.gethostname())
port = 50505

# Starting Plattoning server sistem
plat_system = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
plat_system.bind((host, port))
plat_system.listen()

# Lists For Clients and The Truck_names
clients = []
Truck_names = []
Trucks = []
Distances = []
Matchs = []
Fuels = []
Bodys = []
Sensors = []
Efficiencies = []


# Master truck
m_truck = ''
m_speed = ''

# Sending Messages connected trucks
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Trucks
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing trucks

            global m_truck
            index = clients.index(client)
            t_name = Truck_names[index]
            print(f"t_name {t_name}")
            print(f"m_truck {m_truck}")
            if t_name == m_truck:
                try:
                    print("Lost connection with the master truck!!!!")
                    print(f'Assining master to first slave: {Truck_names[1]}')
                    m_truck = Truck_names[1]
                    clients[1].send('MASTER_TRUCK'.encode(FORMAT))
                except:
                    print("No master truck selected")
                    m_truck = m_truck = ''

            clients.remove(client)
            client.close()
            t_name = Truck_names[index]
            print(f"Lost connection with {t_name}... removing from the system")
            broadcast('{} truck left!'.format(t_name).encode(FORMAT))
            Truck_names.remove(t_name)
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 3}")
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        global m_speed
        client, address = plat_system.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store truck data
        client.send('TRUCK_NAME'.encode(FORMAT))
        t_name = client.recv(1024).decode(FORMAT)
        client.send('DISTANCE'.encode(FORMAT))
        D_cov = client.recv(1024).decode(FORMAT)
        client.send('W_SPEED'.encode(FORMAT))
        temp_speed = client.recv(1024).decode(FORMAT)
        client.send('MATCH'.encode(FORMAT))
        temp_match = client.recv(1024).decode(FORMAT)
        client.send('FUEL'.encode(FORMAT))
        temp_fuel = client.recv(1024).decode(FORMAT)
        client.send('BODY'.encode(FORMAT))
        temp_body = client.recv(1024).decode(FORMAT)
        client.send('SENSORS'.encode(FORMAT))
        temp_sensor = client.recv(1024).decode(FORMAT)
        client.send('EFF'.encode(FORMAT))
        temp_eff = client.recv(1024).decode(FORMAT)

        new_truck = (t_name, D_cov)
        Trucks.append(new_truck)
        Truck_names.append(t_name)
        clients.append(client)
        Matchs.append(temp_match)
        Fuels.append(temp_fuel)
        Bodys.append(temp_body)
        Sensors.append(temp_sensor)
        Efficiencies.append(temp_eff)


        # the first truck will be assigned as a master truck
        if threading.activeCount() == 1:
            global m_truck
            m_truck = t_name
            m_speed = temp_speed
            print(f"New master truck: {m_truck}")
            client.send('MASTER_TRUCK'.encode(FORMAT))
        else:
            print(f'plattooning speed {m_speed}')
            client.send('SLAVE_TRUCK'.encode(FORMAT))
            message = 'C_SPEED {}\n'.format(m_speed)
            client.send(message.encode(FORMAT))

        # Print And Broadcast t_name
        print("Truck id {}".format(t_name))
        broadcast("{} Added to the system".format(t_name).encode(FORMAT))
        client.send('Connected to platooning system!'.encode(FORMAT))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

        #print(f"Active trucks: {Trucks}")
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")

def user_in():
    while True:
        uinput = input(":>")
        if uinput == 'DEEP':
            if threading.activeCount() > 4:
                url = 'https://truckplatooningapi.herokuapp.com/predict'
                truckData = {
                    "TruckName": Truck_names[0], #String
                    "Distance_Covered": int(Distances[0]), #Int
                    "Match_of_Route": int(Matchs[0]),  # 0 for False and 1 for True 
                    "Fuel_Consumption": int(Fuels[0]),  # Int 
                    "Body_Characteristics": int(Bodys[0]), # 1 = bad, 2 = good, 3 = better, 4 = best
                    "Equipment_Sensors": int(Sensors[0]), # Int denoting the number of sensors in the truck
                    "Efficiency": int(Efficiencies[0]),  # 1 = bad, 2 = good, 3 = better, 4 = best
                    "TruckName2": Truck_names[1], #String
                    "Distance_Covered2": int(Distances[1]), #Int
                    "Match_of_Route2": int(Matchs[1]), # 0 for False and 1 for True 
                    "Fuel_Consumption2": int(Fuels[1]), # Int 
                    "Body_Characteristics2": int(Bodys[1]), # 1 = bad, 2 = good, 3 = better, 4 = best
                    "Equipment_Sensors2": int(Sensors[1]),  # Int denoting the number of sensors in the truck
                    "Efficiency2": int(Efficiencies[1]), # 1 = bad, 2 = good, 3 = better, 4 = best
                    "TruckName3": Truck_names[2], #String
                    "Distance_Covered3": int(Distances[2]), #Int
                    "Match_of_Route3": int(Matchs[2]), # 0 for False and 1 for True 
                    "Fuel_Consumption3": int(Fuels[2]), # Int 
                    "Body_Characteristics3": int(Bodys[2]), # 1 = bad, 2 = good, 3 = better, 4 = best
                    "Equipment_Sensors3": int(Sensors[2]), # Int denoting the number of sensors in the truck
                    "Efficiency3": int(Efficiencies[2])  # 1 = bad, 2 = good, 3 = better, 4 = best
                    }

                result = requests.post(url, json=truckData)
                print(result.text)

            else:
                print("Not enough trucks to perform this operation")


inputThread = threading.Thread(target=user_in)
inputThread.start()

print(f"Platooning systems start addr: {host}")
receive()