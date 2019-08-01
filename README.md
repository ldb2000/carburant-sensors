# carburant sensor for home assistant

This custom_component monitor the price of french fuel stations. 

## Installation

You have to install the custom_components/carburant in your custom_components folder.

## configuration.yaml

Creation of a or multiple sensors:

```yaml
sensor:
  - platform: carburant
    list_gas_stations:
      - id1
      - id2
```

id1 or id2 in this example could be retreived from the file PrixCarturants_instantane.xml  

```xml
<pdv id="24100010" latitude="4483300" longitude="49700" cp="24100" pop="R">
    <adresse>15 Route d'Agen - Lespinassat</adresse>
    <ville>BERGERAC</ville>
```

## Example of automation

The configuration.yaml example show some kinds of automation to retreive the cheapest fuel station. 


