from decimal import Decimal
import random
from pytest import fixture

from sweepy.models import RunnerOdds


def _generate_random_id() -> str:
    return str(random.randint(1, int(10e10)))


@fixture
def runner_probabilities_us_open() -> list[RunnerOdds]:
    items = [
        ("Scottie Scheffler", Decimal("0.1894")),
        ("Rory McIlroy", Decimal("0.1024")),
        ("Xander Schauffele", Decimal("0.0550")),
        ("Jon Rahm", Decimal("0.0229")),
        ("Viktor Hovland", Decimal("0.0578")),
        ("Ludvig Aberg", Decimal("0.0480")),
        ("Collin Morikawa", Decimal("0.0425")),
        ("Tommy Fleetwood", Decimal("0.0410")),
        ("Bryson DeChambeau", Decimal("0.0351")),
        ("Brooks Koepka", Decimal("0.0275")),
        ("Shane Lowry", Decimal("0.0322")),
        ("Patrick Cantlay", Decimal("0.0184")),
        ("Max Homa", Decimal("0.0240")),
        ("Cameron Smith", Decimal("0.0244")),
        ("Jordan Spieth", Decimal("0.0109")),
        ("Joaquin Niemann", Decimal("0.0163")),
        ("Hideki Matsuyama", Decimal("0.0155")),
        ("Matt Fitzpatrick", Decimal("0.0150")),
        ("Wyndham Clark", Decimal("0.0161")),
        ("Justin Thomas", Decimal("0.0133")),
        ("Min Woo Lee", Decimal("0.0141")),
        ("Brian Harman", Decimal("0.0105")),
        ("Tyrrell Hatton", Decimal("0.0136")),
        ("Will Zalatoris", Decimal("0.0136")),
        ("Sahith Theegala", Decimal("0.0136")),
        ("Cameron Young", Decimal("0.0088")),
        ("Robert MacIntyre", Decimal("0.0133")),
        ("Dustin Johnson", Decimal("0.0021")),
        ("Tom Kim", Decimal("0.0055")),
        ("Tony Finau", Decimal("0.0073")),
        ("Jason Day", Decimal("0.0073")),
        ("Louis Oosthuizen", Decimal("0.0078")),
        ("Sung-Jae Im", Decimal("0.0020")),
        ("Justin Rose", Decimal("0.0020")),
        ("Alex Noren", Decimal("0.0020")),
        ("Patrick Reed", Decimal("0.0020")),
        ("J.T. Poston", Decimal("0.0019")),
        ("Sam Burns", Decimal("0.0019")),
        ("Russell Henley", Decimal("0.0019")),
        ("Tiger Woods", Decimal("0.0019")),
        ("Si Woo Kim", Decimal("0.0019")),
        ("Ryan Fox", Decimal("0.0019")),
        ("Emiliano Grillo", Decimal("0.0019")),
        ("Adam Scott", Decimal("0.0053")),
        ("Sergio Garcia", Decimal("0.0019")),
        ("Corey Conners", Decimal("0.0019")),
        ("Danny Willett", Decimal("0.0018")),
        ("Adrian Meronk", Decimal("0.0018")),
        ("Chris Kirk", Decimal("0.0018")),
        ("Keegan Bradley", Decimal("0.0018")),
        ("Seamus Power", Decimal("0.0036")),
        ("Kurt Kitayama", Decimal("0.0018")),
        ("Talor Gooch", Decimal("0.0018")),
        ("Thomas Detry", Decimal("0.0018")),
        ("Tom Hoge", Decimal("0.0018")),
        ("Taylor Moore", Decimal("0.0017")),
        ("Keith Mitchell", Decimal("0.0017")),
        ("Matt Wallace", Decimal("0.0017")),
        ("Phil Mickelson", Decimal("0.0017")),
        ("Billy Horschel", Decimal("0.0017")),
        ("Charl Schwartzel", Decimal("0.0017")),
        ("Padraig Harrington", Decimal("0.0017")),
        ("Harris English", Decimal("0.0017")),
        ("Sam Bennett", Decimal("0.0000")),
        ("Mito Pereira", Decimal("0.0016")),
        ("Jordan Smith", Decimal("0.0017")),
        ("Thomas Pieters", Decimal("0.0017")),
        ("Gary Woodland", Decimal("0.0016")),
        ("Alex Fitzpatrick", Decimal("0.0016")),
        ("Abraham Ancer", Decimal("0.0016")),
        ("Matthew Jordan", Decimal("0.0000")),
        ("Zach Johnson", Decimal("0.0015")),
        ("Stewart Cink", Decimal("0.0014")),
        ("Darren Clarke", Decimal("0.0000")),
    ]

    return [
        RunnerOdds(
            provider_id=_generate_random_id(),
            name=name,
            implied_probability=probability,
        )
        for name, probability in items
    ]
