//This file was generated from (Commercial) UPPAAL 4.0.15 rev. CB6BB307F6F681CB, November 2019

/*
Exist a moment when Truck 1 and Truck 2 are master at the same time
*/
E<> Truck1.MasterTruck and Truck2.MasterTruck

/*
If there is a slave truck, it has to be a master truck
*/
A[] Platooning.Slave_ imply Platooning.Master_

/*
No deadlock
*/
A[] not deadlock

/*
can be there three intruders at the same time in between of the same two trucks
*/
E<> Platooning.intrpos_1 == 3

/*
There is only one master
*/
A[] Truck1.MasterTruck imply (Truck2.MasterTruck == false and Truck3.MasterTruck == false)
