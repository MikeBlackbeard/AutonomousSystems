//This file was generated from (Commercial) UPPAAL 4.0.15 rev. CB6BB307F6F681CB, November 2019

/*

*/
E<> Truck1.MasterTruck and Truck2.MasterTruck

/*

*/
E[] Truck1.MasterTruck imply (Platooning.Slave_ == true and Platooning.Slave2_ == true)

/*
Always that the trucks are in the Queue, the three flags for accessing the platooning are on false, which represents avaliable
*/
A[] (Truck1.Que and Truck2.Que and Truck3.Que) imply (Platooning.Master_ == false and Platooning.Slave_ == false and Platooning.Slave2_ == false)

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
