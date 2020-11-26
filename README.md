# TDT4173 Project: Hit Prediction
In this project we are attempting to make supervised predictions of hit songs among the catalogue of songs from 
Billboard charting artists between 2000 and 2020.

###Acknowledgements
It would not be possible to collate a dataset without the following APIs:
- "spotipy": Python module for Spotify's API (https://pypi.org/project/spotipy/)

- "billboard": Python module for Billboard's API (https://pypi.org/project/billboard.py/)

###Installing dependencies
Install with pip:

Spotify API: ```pip install spotipy```

Billboard API: ```pip install billboard.py```

Other dependencies for this project:
```pip install numpy pandas sklearn matplotlib optuna```

##Data
We collate our hit dataset with ```HitDataCollector.py```, fetching all Billboard hits since January 2000 until today.
This dataset is saved as ```billboard.csv``` and consists of roughly 6700 hits after removing songs Spotify could not find properly in the form of karaoke,
cover and non-original versions, or if the artist does not exist on the platform. 

```HitDataCollector.py``` creates ```artist_dataframe.csv``` and iterates through each artist in the ```billboard.csv```
dataset, sampling songs from the catalogue of the artist since January 2000 that does not exists in the hit dataset. 
The flop dataset consists of 37 000 songs.

