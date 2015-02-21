# box-notifer
a tiny network monitoring tool that sends notification whenever someone connects to your local network

#Screenshots

![alt text](http://nsa33.casimages.com/img/2015/02/21/150221041725711485.png "screen1")

![alt text](http://nsa33.casimages.com/img/2015/02/21/15022104182173301.png "screen1")

#How to Use ?
install box-notifier by using

    $ python setup.py install
  
then execute the script using 

    $ ./box-notifier.py -i <interface> -m <methode>
    
example : 

    $ ./box-notifier.py -i wlan0 -m arp
  
  
available argument are 

* -h          #show help
* -i          #set an interface 
* -m          #set methode
* --verbose 


