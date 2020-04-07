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
* water heater (Immersion Rod),
* bucket,
* water temperature sensor (to ensure that heated water does not exceed 40 degrees Celsius)
* pipes
* circulator

![Image](readme_images/heating_top_view.jpg)

This system is energy efficient because, unlike air, water tends to retain its temperature and this helps to keep the greenhouse warm for longer. Another advantage is that the plants are heated gradually (not instantly) and the heat is well distributed (not in one spot).

...

#### Increasing Humidity
...

#### Decreasing Humidity
...

## Substrate Moisture control
Soil humidity sensor manages the operation of the watering system.

#### Watering system
...

## Luminocity control
A photoresistor captures changes in luminocity level.

#### More light
...

#### Less light
...

## pH control
A liquid pH sensor indicates whether pH is out of regular value range, meaning that substrate should be replaced with a new one.
