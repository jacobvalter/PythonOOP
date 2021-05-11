# Objektově orientované programování v Pythonu - základy

Ještě než se pustíme do samotné teorie a praxe s OOP v Pythonu, hned na začátku si řekneme co je cílem naší nové aplikace, ve které budeme používat objekty. Volně také navážeme na zkušenosti z předchozích hodin, které však nejsou nutnou podmínkou.

Chceme vytvořit jednoduchu BI (business intelligence) aplikaci, která bude umět:
- zpracovávat data ze senzorů, načtená z CSV
- strukturovat senzory do jednotlivých zařízení
- vytvářet přehledy, statistiky, grafy pro jednotlivé senzory či zařízení
- ...a další

Díky tomu, že aplikaci budeme psát za použití objektů, dostaneme následující výhody:
- snadné přidání (připojení) nových senzorů a zařízení do aplikace
- snadná rozšiřitelnost aplikace o nové funkce
- přehlednost kódu

Co se naučíme?
- definovat třídy
- vytvářet a používat objekty z vlastních tříd
- namodelovat naší aplikaci
- používat atributy a metody abychom definovali data a chování objektů
- používat speciální funkce tříd (tzv. dunder metody)
- něco málo o dědičnosti (bude rozšířeno v další lekci)
-----

OOP je metoda strukturování kódu (programu) tak, aby data (proměnné) a chování (metody) které spolu souvisejí byly spolu "uzavřeny" (zapouzdřeny, seskupeny) do objektů. Používá se pro znovuvyužití již existujícího kódu, lepší strukturování a zvyšuje přehlednost (samozřejmě je toho mnohem více co OOP přináší). Doteď jsme programovali tzv. procedurálně - používali jsme funkce (procedury) abychom opakovaně využívali nějaký užitečný kód. To nám ve většině případů stačí. Objekty nám umožňují tento koncept rozšířit tak, že si k funkcím "přilepíme" i data a to celé zabalíme do objektu, který můžeme používat dokola a dokola.

V Pythonu objekty využíváme i když to možná netušíme - string, int, list, Pandas DataFrame a další jsou třídy a když s nimi pracujeme, např. ukládáme hodnotu do proměnné tak pracujeme s objektem dané třídy (čti dál a dozvíš se jaký je rozdíl mezi třídou a objektem). Prakticky vše co v Pythonu používáme jsou objekty, jen je to tak chytře skryté, že si to často ani neuvědomujeme. Jsou ale i jiné jazyky jako např. C#, C++, Java, atd.) které rozlišují mezi objektem a hodnotou. My se naučíme jak si vytvořit své vlastní třídy a co všechno nám umožňují.

V OOP je základním pojmem třída (class), někdy se jí také říká typ (type). Třída je něco jako předpis (návrh, vzor, mustr), který říká jak daný objekt vypadá - jaké má atributy (proměnné - data) a jaké má metody (chování). Díky tomu že známe jak je třída definována, máme jistotu, že každý objekt vytvořený z dané třídy má dané atributy a metody - tato skutečnost se nám bude velmi hodit. Třída nám vlastně seskupuje určité proměnné a určité metody do logického celku, který (většinou) dává smysl.

Třída je předpis pro objekt a udává strukturu daného objektu (jeho atributy-data a metody). Objekt je třída naplněná daty (její atributy jako např. název, jméno výrobce, atd. mají už konkrétní hodnotu). Někdy je objekt nazýván instance třídy či instanciovaná třída.

## Modelování tříd
Teď, když už víme co jsou to základní pojmy, pojďme si namodelovat třídy pro naší aplikaci. Ze zadání můžeme vyčíst, že se bavíme o věcech jako je senzor nebo zařízení. To jsou věci - objekty ze skutečného života, které si můžeme snadno představit. Co by tak asi mohl umět a mohl uchovávat senzor v podání naší BI aplikace? Tak určitě by měl mít proměnné jako např. název, dál by mohl obsahovat proměnou pro uchování jednotek, ve které jsou data uložena a rozhodně musí mít proměnnou ve které budou uložena samotná data. Dále se nám u senzoru také bude hodit určité chování - funkce které provedou operace jako "načti data", "vykresli graf", nebo něco jako "spočítej zajímavá čísla" (nebo-li agregáty).

Třída pro zařízení by mohla vypadat např. tak, že má proměnnou jméno, název výrobce a dále pak bude obsahovat všechny přiřazené senzory (např. teplotní a tlakové). Z chování bude mít operace jako "přidej senzor" a "vykresli všechna data". 

## Definice třídy
Vlastní třídu v Pythonu nadefinujeme velmi snadno:
```python
class Equipment:
    name = "undefined"
    vendor = "undefined"

    def details(self):
        print(f"name: {Equipment.name} vendor: {Equipment.vendor}")
```
Za klíčovým slovem class je jméno třídy s dvojtečkou a po odsazení na novém řádku definujeme jeho atributy a metody. V příkladu výše vidíme, že máme 2 atributy - name a vendor které mají počáteční hodnotu undefined a dále je zde metoda details, která zobrazí jméno a výrobce.
Třídy pojmenováváme s velkým počátečním písmenem, aby se nepletla s názvy proměnných, které běžně pojmenováváme s malým počátečním písmenem. K významu parametru self se dostaneme později.

## Použití tříd - vytvoření konkrétního objektu
Třídu použijeme jednoduše:
```python
hotOven = Equipment()

hotOven.name = "Hot Oven"
hotOven.vendor = "United Oven Factories"
hotOven.details()
```

Výsledkem bude:
```
name: Hot Oven vendor: United Oven Factories
```

Jak vidíme z kódu výše tak pomomcí operátoru pro přiřazení vytvoříme novou instanci třídy (podobně jakobychom volali metodu tzn. včetně závorek) a přiřadíme ji dané proměnné. Následně na vytvořeném objektu můžeme přes tečku přistupovat k jejím atributům a nebo volat její metody. Všimněte si, že parametr který je v definici metody details pojmenován jako self při volání této metody nevyplňujeme.

## Atributy - proměnné (data)
Drtivá většina objektů uchovává data, stejně tak jako objekty v našem případě. Výhodou objektů je, že když si vytvořím více objektů jedné třídy tak data přiřazená atributu daného objektu neovlivní data v jiném objektu. To, jakým způsobem definujeme atributy třídy a jak s nimi pracujeme na konkrétním objektu jsme si ukázali výše. Pokud se pokusíme na objektu přistoupit k atributu, který nebyl ve třídě definován, dostaneme chybu.

### Rozsah atributů - atributy třídy a atributy instance
TDB

## Metody (chování) a parameter self
Jak si můžete všimnou tak metoda visualize ve třídě Equipment má právě jeden parameter pojmenovaný self. self je speciální jméno pro parameter, díky kterému můžeme v těle definované metody přistupovat k atributům a metodám objektu se kterým se pracuje - odkazuje na objekt samotný. Všechny metody každé třídy jej musí obsahovat a to právě jako první parameter. Následně za ním mohou být parametry další, jako můžete vidět v následujícím příkladě třídy Sensor:

```python
class Sensor:
    units = "unknown"
    data = pd.DataFrame()

    def load_data(self, csvPath):
        self.data = pd.read_csv(csvPath, header = None, delimiter = ";")
        self.data.columns = ["timestamp","value"]
        self.data.name = csvPath[0:name_csv_files[i].index(".")]
```

## Konstruktor nebo-li \_\_init\_\_
Často se stane, že některá data v našem objektu (v instanci třídy) nesmí chybět - jako např. název zařízení nebo senzoru. Jednoduše chceme, aby určitá data objektu musela být zadána při vytváření objektu. Toho se dá docílit speciální metodou, tzv. konstrukorem. Tato metoda se zavolá vždy, když se vytváří nová instance objektu. Kromě toho, že si díky konstruktoru můžeme vynutit, aby byla při vytváření objektu zadána nějaká data, která jsou důležitá, lze konstruktor použít i pro provedeni nějakých operací či úkonů, které nám správně nastaví (nebo-li inicializují) nový objekt. V našem případě chceme zajistit aby každý senzor nebo zařízení mělo vždy nějaké jméno a nebylo jen "undefined". V Pythonu se konstruktor definuje pomocí tzv. "magic" nebo také "dunder" metodou __init__:

```python
class Sensor:
    units = "unknown"
    data = pd.DataFrame()
    def __init__(self, name):
        self.name = name

    def load_data(self, csvPath):
        self.data = pd.read_csv(csvPath, header = None, delimiter = ";")
        self.data.columns = ["timestamp","value"]
        self.data.name = csvPath[0:name_csv_files[i].index(".")]
```

V kódu výše je vidět definice metody \_\_init\_\_ s parametrem self - to proto abychom mohli přistupovat k atributům nebo metodám objektu, a dále pak s parametrem name abychom vynutili zadání parametru při vytváření objektu (instance třídy Sensor). V těle metody už jen jednoduše přiřazujeme hodnotu parametru name do atributu name, který patří k objektu (přes self). Všimněte si, že nemusíme atribut name definovat jinde ve třídě, stačí jej jen takto určit v kontruktoru. 

Když nyní budeme objekt pro senzor vytvářet, musíme uvést jeho jméno:
```python
temperatureSensor = Sensor("Upper Part Temperature")
```

Pokud jej neuvedeme a zavoláme jen:
```python
temperatureSensor = Sensor()
```
pak dostaneme chybu.

## Dunder metody
Dunder znamená double-under nebo-li metody se zvlášťním významem. Už jsme poznali metodu __init__, jsou zde všas i další:
\_\_str\_\_ a \_\_repr\_\_
\_\_len\_\_
\_\_getitem\_\_
\_\_reversed\_\_

\_\_eq\_\_
\_\_gt\_\_
\_\_add\_\_

## Ověření typu objektu
TDB

## Operátory
TDB

## Dědičnost
TDB

## Propojení s knihovnami
TDB