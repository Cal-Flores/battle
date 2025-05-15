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
  "Adult Gon",
  "Akatsuki Sasuke",
  "Aki",
  "Amaterasu Sasuke",
  "Android 18",
  "Anbu Itachi",
  "Anbu Kakashi",
  "Armor Titan",
  "Asuma",
  "Attack Titan",
  "Beast Titan",
  "Bisky",
  "Bonolenov",
  "Cart Titan",
  "Chainsaw Man",
  "Choji",
  "Chrollo",
  "Colossal Titan",
  "Deidara",
  "Erza",
  "Feitan",
  "Female Titan",
  "Franklin",
  "Gaara",
  "Geto",
  "Ging",
  "Gohan",
  "Goku",
  "Godspeed Killua",
  "Gojo",
  "Gon",
  "Hashirama",
  "Hanzo",
  "Himeno",
  "Hidan",
  "Hinata",
  "Hisoka",
  "Hunter Killua",
  "Ikalgo",
  "Illumi",
  "Ino",
  "Itachi",
  "Jaw Titan",
  "Jiraiya",
  "Juubito",
  "Kabuto",
  "Kaguya",
  "Kakashi",
  "Kakuzu",
  "Kalluto",
  "Kankuro",
  "Karin",
  "Kasumi",
  "Katana Man",
  "Kenjaku",
  "Killer Bee",
  "Killua",
  "Kishibe",
  "Kisame",
  "Kite",
  "Knuckle",
  "Kobeni",
  "Koga",
  "Konan",
  "Kurama",
  "Kurapika",
  "Leorio",
  "Levi",
  "Madara",
  "Machi",
  "Maki",
  "Mai",
  "Mahito",
  "Makima",
  "Menthuthuyoupi",
  "Mechamaru",
  "Megumi",
  "Mei Mei",
  "Melody",
  "Meruem",
  "Might Guy",
  "Mikasa",
  "Minato",
  "Momo",
  "Nanami",
  "Naruto",
  "Natsu",
  "Neferpitou",
  "Neji",
  "Netero",
  "Nobara",
  "Nobunaga",
  "Noritoshi",
  "Obito",
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
  "Rock Lee",
  "Sai",
  "Sage Naruto",
  "Sakura",
  "Sasori",
  "Sasuke",
  "Shaiapouf",
  "Shalnark",
  "Shikamaru",
  "Shino",
  "Shizuku",
  "Shoko",
  "Shukaku",
  "Six Paths Naruto",
  "Suigetsu",
  "Sukuna",
  "Temari",
  "Todo",
  "Toji",
  "Tobe",
  "Tobirama",
  "Toge",
  "Trunks",
  "Tsunade",
  "Utahime",
  "Uvogin",
  "Vegeta",
  "Yamato",
  "Yuki",
  "Yuji",
  "Zetsu"
]

names = [
  "Adult Gon",
  "Akatsuki Sasuke",
  "Aki",
  "Amaterasu Sasuke",
  "Android 18",
  "Anbu Itachi",
  "Anbu Kakashi",
  "Armor Titan",
  "Asuma",
  "Attack Titan",
  "Beast Titan",
  "Bisky",
  "Bonolenov",
  "Cart Titan",
  "Chainsaw Man",
  "Choji",
  "Chrollo",
  "Colossal Titan",
  "Deidara",
  "Erza",
  "Feitan",
  "Female Titan",
  "Franklin",
  "Gaara",
  "Geto",
  "Ging",
  "Gohan",
  "Goku",
  "Godspeed Killua",
  "Gojo",
  "Gon",
  "Hashirama",
  "Hanzo",
  "Himeno",
  "Hidan",
  "Hinata",
  "Hisoka",
  "Hunter Killua",
  "Ikalgo",
  "Illumi",
  "Ino",
  "Itachi",
  "Jaw Titan",
  "Jiraiya",
  "Juubito",
  "Kabuto",
  "Kaguya",
  "Kakashi",
  "Kakuzu",
  "Kalluto",
  "Kankuro",
  "Karin",
  "Kasumi",
  "Katana Man",
  "Kenjaku",
  "Killer Bee",
  "Killua",
  "Kishibe",
  "Kisame",
  "Kite",
  "Knuckle",
  "Kobeni",
  "Koga",
  "Konan",
  "Kurama",
  "Kurapika",
  "Leorio",
  "Levi",
  "Madara",
  "Machi",
  "Maki",
  "Mai",
  "Mahito",
  "Makima",
  "Menthuthuyoupi",
  "Mechamaru",
  "Megumi",
  "Mei Mei",
  "Melody",
  "Meruem",
  "Might Guy",
  "Mikasa",
  "Minato",
  "Momo",
  "Nanami",
  "Naruto",
  "Natsu",
  "Neferpitou",
  "Neji",
  "Netero",
  "Nobara",
  "Nobunaga",
  "Noritoshi",
  "Obito",
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
  "Rock Lee",
  "Sai",
  "Sage Naruto",
  "Sakura",
  "Sasori",
  "Sasuke",
  "Shaiapouf",
  "Shalnark",
  "Shikamaru",
  "Shino",
  "Shizuku",
  "Shoko",
  "Shukaku",
  "Six Paths Naruto",
  "Suigetsu",
  "Sukuna",
  "Temari",
  "Todo",
  "Toji",
  "Tobe",
  "Tobirama",
  "Toge",
  "Trunks",
  "Tsunade",
  "Utahime",
  "Uvogin",
  "Vegeta",
  "Yamato",
  "Yuki",
  "Yuji",
  "Zetsu"
]


images = sorted(unsorted_images)

rounds = [
    'Consolation Round',
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
    score = IntegerField('Score')
    tournamnet = StringField('Tournament')
    round = SelectField('Round', choices=rounds)
    submit = SubmitField('Submit')

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
