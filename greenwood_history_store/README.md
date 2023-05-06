# Data store for the Greenwood mapping project

Django app that stores structural relational data for the Greenwood mapping project.

## Development setup
Efforts have been made to make setup of this project easy for new contributors and only requires a few local prerequisites.

Prerequisites: 

* [Docker desktop](https://www.docker.com/products/docker-desktop/)
* [Vscode](https://code.visualstudio.com/)
  * with [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension installed
* Parcel and addresses data
  * both have objectid property, do they change?

## MVP Interface needs
  Be able to click on a point (What is a point? addresses? POI?)
  Possibly clicking on a block boundary and seeing all related data inside it over the years and list of losses.
  1920 census data
  what we know about a place over time

Polk data is in the upload files version directory, need to import and make relations to addresses and 

## MVP Backend needs
* Import all the data from the polk data
* Add pg-history to track changes to imported data.
* Add a canonical ref for entities?
* How to track entities that are named differently or import data that need.

# TODO
How to deal with GIS?
Setup github actions to run django tests.

# Questions
* integrations with arcGIS?
  * Use arcGIs for most of the application? mapping interaction?