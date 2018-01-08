# crawl-battles

https://play.pokemonshowdown.com/
の対戦結果をクローリングする。


## How to use

```
docker build -t ${IMAGENAME} .
docker run --rm -v ${FULLPATH-to-CurrentDirectory}:/app -w=/app -it ${IMAGENAME} python3 main.py
```
