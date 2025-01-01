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


unsorted_images = ['akat-sas.jpeg', 'anbu-itachi.jpeg', 'asuma.jpeg','beat-nar.jpeg','beat-sas.jpeg','killer_bee.jpeg','bunta.webp','chakra.jpeg','choji.webp',
'cursed.jpeg', 'dadara.jpeg', 'deidara.webp', 'gaara.jpeg', 'guy.jpeg', 'hashirama.webp', 'hidan.jpeg','hinata.jpeg', 'ino.webp', 'massacre.jpeg',
'itachi.jpeg', 'jiraiya.jpeg', 'jutsu.jpeg', 'juubito.jpeg', 'kabuto.webp', 'kaguya.jpeg', 'anbu_kakashi.webp', 'kankuro.jpeg', 'karin.webp', 'kiba.jpeg', 'kichi.webp',
'konan.jpeg', 'kurama.jpeg', 'madara.gif', 'minato.jpeg', 'neji.jpeg', 'obito.webp', 'orochimaru.jpeg', 'pain.webp', 'rage.webp', 'ramen.jpeg', 'regkak.jpeg',
'regsas.jpeg', 'rock.jpeg', 'sage.gif', 'sai.webp', 'sakura.jpeg', 'amaterasu.jpeg', 'sasori.png', 'shikamaru.jpeg', 'shino.jpeg', 'shukaku.jpeg', 'shuriken.jpeg',
'six-paths-sage.jpeg', 'suigetsu.webp', 'sword.jpeg', 'temari.webp', 'tobi.webp', 'tobirama.webp', 'tsunade.webp', 'sharigankak.webp', 'warsakura.jpeg', 'yamato.webp', 'zetsu.png'
]

names = [
    "Akatsuki Sasuke",
"Amaterasu Sasuke",
"Anbu Itachi",
"Anbu Kakashi",
"Asuma",
"Beat Naruto",
"Beat Sasuke",
"Chakra Naruto",
"Choji",
"Cursed Hidan",
"Dadara",
"Deidara",
"Gaara",
"Gamabunta",
"Gamakichi",
"Hashirama",
"Hiroku",
"Hidan",
"Hinata",
"Ino",
"Itachi",
"Jiraiya",
"Jutsu Naruto",
"Juubito",
"Kabuto",
"Kaguya",
"Kakashi",
"Kankuro",
"Karin",
"Kiba",
"Killer Bee",
"Konan",
"Kurama",
"Madara",
"Masked Man",
"Massacre Itachi",
"Might Guy",
"Minato",
"Neji",
"Obito",
"Orochimaru",
"Pain",
"Rage Tobi",
"Ramen Naruto",
"Rock Lee",
"Sage Naruto",
"Sai",
"Sakura",
"Sasori",
"Sasuke",
"Sharingan Kakashi",
"Shikamaru",
"Shino",
"Shukaku",
"Shuriken Naruto",
"Six Paths Naruto",
"Suigetsu",
"Sword Sasuke",
"Temari",
"Tobirama",
"Tsunade",
"War Sakura",
"Yamato",
"Zetsu",
]

images = sorted(unsorted_images)

rounds = [
    'Consolation Round',
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
    'Cons-Semi',
    'Cons-Quarter',
    'Blood Round',
    'Round of 12',
    'Cons-24',
    'Cons-16'
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
    ]

class NewTour(FlaskForm):
    link = StringField('Link')
    name = StringField('Name')
    date = DateField('Date')
    first = SelectField("First", choices=images)
    second = SelectField('Second', choices=images)
    third = SelectField('Third', choices=images)
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
    tournamnet = IntegerField('Tournament')
    round = SelectField('Round', choices=rounds)
    submit = SubmitField('Submit')

class NewHistory(FlaskForm):
    player_1 = StringField('Fighter 1')
    player_2 = StringField('Fighter 2')
    submit = SubmitField('Submit')

class Search(FlaskForm):
    name = StringField('Name')
    round = SelectField('Round', choices=search_rounds)
    leaders = BooleanField('Leaders')
    win_percent = BooleanField('Win Percent')
    submit = SubmitField('Submit')
