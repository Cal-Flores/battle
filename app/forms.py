from flask_wtf import FlaskForm
from wtforms import DateField, StringField, IntegerField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


class NewPlayer(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    wins = IntegerField('Wins')
    loss = IntegerField('Loss')
    points = IntegerField('Points')
    img = StringField('Img')
    gold = IntegerField('Gold')
    silver = IntegerField('Silver')
    bronze = IntegerField('Bronze')
    medal = IntegerField('Medal')
    submit = SubmitField('Submit')


class EditPlayer(FlaskForm):
    wins = IntegerField('Wins')
    loss = IntegerField('Loss')
    points = IntegerField('Points')
    gold = IntegerField('Gold')
    silver = IntegerField('Silver')
    bronze = IntegerField('Bronze')
    medal = IntegerField('Medal')
    badge = IntegerField('Badge')
    submit = SubmitField('Submit')


# unsorted_images = ['akat-sas.jpeg', 'anbu-itachi.jpeg', 'asuma.jpeg','beat-nar.jpeg','beat-sas.jpeg','killer_bee.jpeg','bunta.webp','chakra.jpeg','choji.webp',
# 'cursed.jpeg', 'dadara.jpeg', 'deidara.webp', 'gaara.jpeg', 'guy.jpeg', 'hashirama.webp', 'hidan.jpeg','hinata.jpeg', 'ino.webp', 'massacre.jpeg',
# 'itachi.jpeg', 'jiraiya.jpeg', 'jutsu.jpeg', 'juubito.jpeg', 'kabuto.webp', 'kaguya.jpeg', 'anbu_kakashi.webp', 'kankuro.jpeg', 'karin.webp', 'kiba.jpeg', 'kichi.webp',
# 'konan.jpeg', 'kurama.jpeg', 'madara.gif', 'minato.jpeg', 'neji.jpeg', 'obito.webp', 'orochimaru.jpeg', 'pain.webp', 'rage.webp', 'ramen.jpeg', 'regkak.jpeg',
# 'regsas.jpeg', 'rock.jpeg', 'sage.gif', 'sai.webp', 'sakura.jpeg', 'amaterasu.jpeg', 'sasori.png', 'shikamaru.jpeg', 'shino.jpeg', 'shukaku.jpeg', 'shuriken.jpeg',
# 'six-paths-sage.jpeg', 'suigetsu.webp', 'sword.jpeg', 'temari.webp', 'tobi.webp', 'tobirama.webp', 'tsunade.webp', 'sharigankak.webp', 'warsakura.jpeg', 'yamato.webp', 'zetsu.png'
# ]

unsorted_images = [

  "Abyss",
"Adult Gon",
"Akatsuki Sasuke",
"Aki",
"Alex Louis",
"Alphonse",
"Amaterasu Sasuke",
"Anbu Itachi",
"Anbu Kakashi",
"Android 18",
"Armor Titan",
"Asta",
"Asuma",
"Attack Titan",
"Beast Titan",
"Bisky",
"Bonolenov",
"Byakuya",
"Cammy",
"Cart Titan",
"Cell",
"Chainsaw Man",
"Chakra Naruto",
"Choji",
"Choso",
"Chrollo",
"Chun-Li",
"Colossal Titan",
"Deidara",
"Dot",
"Edward",
"Envy",
"Erwin",
"Erza",
"Feitan",
"Female Titan",
"Fern",
"Flamme",
"Franklin",
"Frieren",
"Frieza",
"Fubuki",
"Gaara",
"Geto",
"Ging",
"Godspeed Killua",
"Gohan",
"Gojo",
"Goku",
"Gon",
"Gotoh",
"Gray",
"Greed",
"Hanzo",
"Hashirama",
"Hidan",
"Himeno",
"Hinata",
"Hisoka",
"Hitsugaya",
"Ichigo",
"Ikalgo",
"Illumi",
"Ino",
"Inosuke",
"Itachi",
"Jaw Titan",
"Jellal",
"Jiraiya",
"Juubi",
"Juubito",
"Kaguya",
"Kaiju No. 8",
"Kakashi",
"Kakuzu",
"Kalluto",
"Kankuro",
"Kasumi",
"Katana Man",
"Kenjaku",
"Kiba",
"Kikoru",
"Killer Bee",
"Killua",
"Kisame",
"Kishibe",
"Kite",
"Knuckle",
"Kobeni",
"Konan",
"Kurama",
"Kurapika",
"Lance",
"Laxus",
"Leorio",
"Levi",
"Ling",
"Luffy",
"Lust",
"Machi",
"Madara",
"Mahito",
"Mai",
"Majin Buu",
"Maki",
"Makima",
"Mash",
"May",
"Mechamaru",
"Megumi",
"Mei Mei",
"Menthuthuyoupi",
"Meruem",
"Might Guy",
"Mikasa",
"Mina",
"Minato",
"Momo",
"Muzan",
"Nami",
"Nanami",
"Natsu",
"Neferpitou",
"Neji",
"Netero",
"Nezuko",
"Nobara",
"Nobunaga",
"Noelle",
"Noritoshi",
"Obito",
"Olivier",
"Orochimaru",
"Pain",
"Pakunoda",
"Panda",
"Phinks",
"Piccolo",
"Pokkle",
"Ponzu",
"Power",
"Rage Tobi",
"Rayne",
"Renji",
"Reno",
"Reze",
"Riza",
"Rock Lee",
"Roy",
"Rukia",
"Sage Naruto",
"Sai",
"Saitama",
"Sakura",
"Sasori",
"Sasuke",
"Scar",
"Shaiapouf",
"Shalnark",
"Shikamaru",
"Shino",
"Shisui",
"Shizuku",
"Shukaku",
"Silva",
"Six Paths Naruto",
"Soshiro",
"Stark",
"Suigetsu",
"Sukuna",
"Tanjiro",
"Tatsumaki",
"Temari",
"Tobirama",
"Todo",
"Toge",
"Toji",
"Trunks",
"Tsunade",
"Uryū",
"Utahime",
"Uvogin",
"Vegeta",
"Walker",
"Yamato",
"Yamamoto",
"Yoruichi",
"Yuji",
"Yuki",
"Yuno",
"Zenitsu",
"Zoro",
"Sheele"
"Bulat",
"Esdeath",
"Akame",
"Tatsumi",
"Mine",
"Leone",
"Kurome",
"Seryu",
"Toa & Ju Fa",
"Gabimaru",
"Sagiri",
"Chobei",
"Yuzuriha",
"Shion",
"Gantetsusai",
'Tao & Ju Fa'
]

names = [
 "Abyss",
"Adult Gon",
"Akatsuki Sasuke",
"Aki",
"Alex Louis",
"Alphonse",
"Amaterasu Sasuke",
"Anbu Itachi",
"Anbu Kakashi",
"Android 18",
"Armor Titan",
"Asuma",
"Attack Titan",
"Beast Titan",
"Bisky",
"Bonolenov",
"Cart Titan",
"Cell",
"Chainsaw Man",
"Chakra Naruto",
"Choji",
"Choso",
"Chrollo",
"Colossal Titan",
"Deidara",
"Dot",
"Edward",
"Envy",
"Erwin",
"Erza",
"Feitan",
"Female Titan",
"Fern",
"Franklin",
"Frieren",
"Frieza",
"Gaara",
"Geto",
"Ging",
"Godspeed Killua",
"Gohan",
"Gojo",
"Goku",
"Gon",
"Gotoh",
"Gray",
"Greed",
"Hanzo",
"Hashirama",
"Hidan",
"Himeno",
"Hinata",
"Hisoka",
"Ikalgo",
"Illumi",
"Ino",
"Itachi",
"Jaw Titan",
"Jiraiya",
"Juubito",
"Kaguya",
"Kaiju No. 8",
"Kakashi",
"Kakuzu",
"Kalluto",
"Kankuro",
"Kasumi",
"Katana Man",
"Kenjaku",
"Kiba",
"Kikoru",
"Killer Bee",
"Killua",
"Kisame",
"Kishibe",
"Kite",
"Knuckle",
"Kobeni",
"Konan",
"Kurama",
"Kurapika",
"Lance",
"Leorio",
"Levi",
"Ling",
"Lust",
"Machi",
"Madara",
"Mahito",
"Mai",
"Maki",
"Makima",
"Mash",
"May",
"Mechamaru",
"Megumi",
"Mei Mei",
"Menthuthuyoupi",
"Meruem",
"Might Guy",
"Mikasa",
"Mina",
"Minato",
"Momo",
"Nanami",
"Natsu",
"Neferpitou",
"Neji",
"Netero",
"Nobara",
"Nobunaga",
"Noritoshi",
"Obito",
"Olivier",
"Orochimaru",
"Pain",
"Pakunoda",
"Panda",
"Phinks",
"Piccolo",
"Pokkle",
"Ponzu",
"Power",
"Rage Tobi",
"Rayne",
"Reno",
"Riza",
"Rock Lee",
"Roy",
"Sage Naruto",
"Sai",
"Sakura",
"Sasori",
"Sasuke",
"Scar",
"Shaiapouf",
"Shalnark",
"Shikamaru",
"Shino",
"Shisui",
"Shizuku",
"Shukaku",
"Silva",
"Six Paths Naruto",
"Soshiro",
"Stark",
"Suigetsu",
"Sukuna",
"Temari",
"Tobirama",
"Todo",
"Toge",
"Toji",
"Trunks",
"Tsunade",
"Utahime",
"Uvogin",
"Vegeta",
"Walker",
"Yamato",
"Yuji",
"Yuki",
]


images = sorted(unsorted_images)

rounds = [
    'Consolation Round',
    'Consolation Round 2',
    'Consolation Round 3',
    'Round of 256',
    'Round of 128',
    'Round of 64',
    'Round of 32',
    'Round of 16',
    'Quarter-Final',
    'Semi-Final',
    'Gold Medal Match',
    'Bronze Medal Match',
    '5th Place Match',
    '7th Place Match',
    '9th Place Match',
    '11th Place Match',
    '13th Place Match',
    '15th Place Match',
    'Cons-Semi',
    'Cons-Quarter',
    'Cons-12',
    'Cons-16',
    'Blood Round',
    'Cons-32',
    'Cons-48',
    'Cons-64',
    'Placement Round',
    'Dual',
    ]
search_rounds = [
    '.',
    'Gold Medal Match',
    'Bronze Medal Match',
    '5th Place Match',
    '7th Place Match',
    '9th Place Match',
    'All Medal Rounds',
    'Semi-Final',
    'Quarter-Final',
    'Round of 16',
    'Round of 32',
    'Round of 64',
    'Cons-Semi',
    'Cons-Quarter',
    'Blood Round',
    'Round of 12',
    'Cons-16',
    'Cons-24',
    'Consolation Round',
    'Consolation Round 2',
    'Consolation Round 3',
    'Dual',
    ''
    ]

class NewTour(FlaskForm):
    link = StringField('Link')
    name = StringField('Name')
    date = DateField('Date')
    # first = SelectField("First", choices=images)
    # second = SelectField('Second', choices=images)
    # third = SelectField('Third', choices=images)
    submit = SubmitField('Submit')


class NewResult(FlaskForm):
    first = SelectField('Champion', choices = images)
    second = SelectField('Runner-up', choices=images)
    third = SelectField('Bronze', choices=images)
    fourth = SelectField('Fourth', choices=images)
    fifth = SelectField('Fifth', choices=images)
    sixth = SelectField('Sixth', choices=images)
    seventh = SelectField('Seventh', choices=images)
    eigth = SelectField('Eigth', choices=images)
    ninth = SelectField('Ninth', choices=images)
    tenth = SelectField('Tenth', choices=images)
    eleventh = SelectField('Eleventh', choices=images)
    twelfth = SelectField('Twelfth', choices=images)
    thirtenth = SelectField('Thirtenth', choices=images)
    fourtenth = SelectField('Fourtenth', choices=images)
    fifthtenth = SelectField('Fifthtenth', choices=images)
    sixtenth = SelectField('Sixtenth', choices=images)
    submit = SubmitField('Submit')


class NewOpponent(FlaskForm):
    name = SelectField('Oppenent Name', choices=names)
    victory = BooleanField('Victory')
    is_ressist = BooleanField('Victory')
    fotn = BooleanField('Victory')
    score = IntegerField('Score')
    tournamnet = StringField('Tournament')
    round = SelectField('Round', choices=rounds)
    submit = SubmitField('Submit')

class EditOpponent(FlaskForm):
    name = SelectField('Oppenent Name', choices=names)
    victory = BooleanField('Victory')
    tournamnet = StringField('Tournament')
    round = SelectField('Round', choices=rounds)
    submit = SubmitField('Submit')


class NewBattle(FlaskForm):
    player_1 = StringField('Fighter 1')
    victory_1 = BooleanField('Victory')
    player_2 = StringField('Fighter 2')
    victory_2 = BooleanField('Victory')
    is_ressist = BooleanField('is_ressist')
    fotn = BooleanField('fotn')
    score = IntegerField('Score')
    tournamnet = StringField('Tournament')
    round = SelectField('Round', choices=rounds)
    submit = SubmitField(
    'Submit',
    render_kw={'class': 'newbattle-submit-btn'}
)

class NewHistory(FlaskForm):
    player_1 = StringField('Fighter 1')
    player_2 = StringField('Fighter 2')
    team_1 = StringField('Team 1')
    team_2 = StringField('Team 2')
    submit = SubmitField('Submit')

class Search(FlaskForm):
    name = StringField('Name')
    round = SelectField('Round', choices=search_rounds)
    leaders = BooleanField('Leaders')
    win_percent = BooleanField('Win Percent')
    submit = SubmitField('Submit')

class NewDual(FlaskForm):
    home = StringField('Home')
    away = StringField('Away')
    week = StringField('Week')
    hscore = IntegerField('Hscore')
    ascore = IntegerField('Ascore')
    winner = StringField('Winner')
    submit = SubmitField('Submit')
