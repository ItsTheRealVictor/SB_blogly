from app import User

first_names = [
    'Dale',
    'Bill',
    'Boom',
    'Peggy',
    'Bobby',
    'John',
    'Khan',
    'Joseph'
]
last_names = [
    'Gribble',
    'Dautrieve',
    'Hauer',
    'Hill',
    'Hill',
    'Redcorn',
    'Souphanousinphone',
    'Gribble'
]

full_names= [User(first_name=first, last_name=last) for first, last in zip(first_names, last_names)]