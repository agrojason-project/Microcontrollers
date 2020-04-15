# Microcontroller Developers (MD) Team

## The duties of a MD
The MD team programs microcontrollers (ie Arduino) and makes sure that every sensor is well calibrated and returns right measurements. The team also suggests solutions on the mechanics of the greenhouse and is responsible for the implementation of the automations. 

## Temperature & Humidity control
Two DHT11 sensors measure temperature and humidity inside and outside the greenhouse.

#### Cooling system
...

#### Heating system
A system similar to underfloor heating will be used. The heating system has one bucket with water. Water is heated with the help of a water heater / immersion rod. 

![Image](readme_images/heating_rod.png)

The heater’s operation is controlled by Arduino microcontroller. Hot water flows through pipes covering the entire floor of the greenhouse. These pipes are under the plants, taking advantage of the fact that hot air moves up.

The heating system consists of:
* water heater (Immersion Rod)
* bucket
* water temperature sensor (to ensure that heated water does not exceed 40 degrees Celsius)
* pipes
* circulator

![Image](readme_images/heating_top_view.jpg)

This system is energy efficient because, unlike air, water tends to retain its temperature and this helps to keep the greenhouse warm for longer. Another advantage is that the plants are heated gradually (not instantly) and the heat is well distributed (not in one spot).

#### Increasing Humidity
...

#### Decreasing Humidity
...

## Substrate Moisture control
Soil humidity sensor manages the operation of the watering system.

#### Watering system
The watering system that we have in this project is simillar to those that implement the process of irrigation in the fields and especially in greenhouses.

The watering system consists of the following components:
	1) The main (central) pipes of water.
	2) An electrovalve
	3) A relay
	4) The smaller pipes that end up inside the greenhouse.
	
To begin with, water flows through the central pipes until it reaches to the electrovalve.
The electrovalve is an electrical component which has a throttle valve at the inside of it's structure. We want to regulate approprietely at any moment if the water will pass in order to water the plants in greenhouse or if it has to be blocked because it will be needless to water our plants. 
When we want to allow the water flow towards the greenhouse the relay which is controled by arduino and is connected suitably in our electrical circuit, will give a signal to the electrovalve and then the throttle valve will open for the water to pass. The same thing happens when we want to stop the water flow and of course then the valve will close.

Finally, it is worth to be mentioned that once the water passes from the electrovalve mechanism then it will be 
splitted to the smaller pipes in order to water our plants in the greenhouse.

This automation of watering system helps us control the water flow with a more effective way 
and also contributes to reduce significantly the amount of water that is wasted with no reason.

## Luminocity control
A photoresistor captures changes in luminocity level.

#### More light
...

#### Less light
...

## pH control
A liquid pH sensor indicates whether pH is out of regular value range, meaning that substrate should be replaced with a new one.
