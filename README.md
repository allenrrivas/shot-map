# shot-map

### Description

This short project was to understand how web scrapping worked and to learn about data analysis in football (soccer). <br><br>
Data from https://understat.com <br>

### Install

    git clone https://github.com/allenrrivas/shot-map.git

### Dependencies

    pip3 install -r requirements.txt

### Execute

Available Shot Types: GOALS, SHOTS-ON-POST, SAVED-SHOTS, BLOCKED-SHOTS, MISSED-SHOTS.

```
cd shot-map
python3 ShotMap.py [understat player url] [shot type]
```

### Example

    python3 ShotMap.py https://understat.com/player/8260 Goals

![HaalandGoals](https://github.com/allenrrivas/shot-map/assets/44716681/e22dfec4-6ccc-4dc7-b866-e85a7752df62)
