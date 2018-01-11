# crawl-battles

[Pokémon Showdown!](https://play.pokemonshowdown.com)の対戦結果を取得する。

## 使い方

### Dockerをつかう場合

```bash
# Dockerを動作させる環境は前提とする。
docker build -t ${IMAGENAME} .
docker run --rm -v ${FULLPATH-to-CurrentDirectory}:/app -w=/app --shm-size=2g -it $
{IMAGENAME} python3 main.py
```

### Dockerをつかわない場合

* Google Chromeをインストールする
* Chrome Driverをインストールする(ヘッドレス対応のバージョンが望ましい)
* 必要なライブラリSelenium,BeautifulSoup4をPython環境にインストールする
