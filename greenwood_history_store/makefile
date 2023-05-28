.ONESHELL:

# TODO: parcel import reference correction
parcels:
	shp2pgsql \
		-d \
		-D \
		-I \
		data/shape/Parcels_20220929/PARCELS220929.shp \
		parcels \
		| psql 

quarters:
	shp2pgsql \
		-d \
		-D \
		-I \
		data/shape/Quarters/quarter.shp \
		quarters \
		| psql 

townships:
	shp2pgsql \
		-d \
		-D \
		-I \
		data/shape/Township/township.shp \
		townships \
		| psql 

models:
	poetry run python ./manage.py inspectdb parcels quarters townships > greenwood_history/apps/shapes/models.py

migrate:
	poetry run python ./manage.py migrate

all: parcels quarters townships models

.PHONY: all
