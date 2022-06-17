import threading
import socket

FORMAT = 'utf-8'

# Connection Data
host = socket.gethostbyname(socket.gethostname())
port = 50505

# Starting plat_system
plat_system = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
plat_system.bind((host, port))
plat_system.listen()

# Lists For Clients and The Truck_names
clients = []
Truck_names = []
Trucks = []

# Master truck
m_truck = ''
m_speed = ''

# Sending Messages connected trucks
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
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
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")
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
        new_truck = (t_name, D_cov)
        Trucks.append(new_truck)
        Truck_names.append(t_name)
        clients.append(client)

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
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print(f"Platooning systems start addr: {host}")
receive()