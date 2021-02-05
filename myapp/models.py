from django.db import models


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/')

av_pos = (
    ('small','small'),
    ('medium', 'medium'),
    ('large','large'),
    ('*', '*')
)

skpvEsco = (
    ('<5','<5'),
    ('5-10', '5-10'),
    ('>10','>10'),
    ('*', '*')
)

lang = (
    ('no','no'),
    ('yes', 'yes'),
    ('*', '*')
)

driv = (
    ('no','no'),
    ('yes', 'yes'),
    ('*', '*')
)

ageapr = (
    ('no','no'),
    ('yes', 'yes'),
    ('*', '*')
)

disapr = (
    ('no','no'),
    ('yes', 'yes'),
    ('*', '*')
)

skpwish = (
    ('no','no'),
    ('yes', 'yes'),
    ('*', '*')
)

bowishct = (
    ('part time','part time'),
    ('not important', 'not important'),
    ('>full time','>full time'),
    ('*', '*')
)

jobctrtype = (
    ('part time','part time'),
    ('full time', 'full time'),
    ('*', '*')
)

bocrwish = (
    ('downgrade','downgrade'),
    ('same', 'same'),
    ('>upgrade career','>upgrade career'),
    ('*', '*')
)

jobcradv = (
    ('down','down'),
    ('same', 'same'),
    ('>up','>up'),
    ('*', '*')
)

bowhwish = (
    ('daily shift','daily shift'),
    ('daily/night shift', 'daily/night shift'),
    ('*', '*')
)

jobwh = (
    ('daily shift','daily shift'),
    ('daily/night shift', 'daily/night shift'),
    ('*', '*')
)

# stavi na srednoto razmah izmegju 10 i 20 ako ima error na prviot del
msoo = (
    ('<10','<10'),
    ('10-20', '10 - 20'),
    ('>20','>20'),
    ('*', '*')
)

bowishloc = (
    ('no','no'),
    ('yes', 'yes'),
    ('*', '*')
)

class Polinja(models.Model):
    Available_positions = models.CharField(max_length=20, choices=av_pos, default='*')
    SKPvsESCO = models.CharField(max_length=20, choices=skpvEsco, default='*')
    Languages = models.CharField(max_length=20, choices=lang, default='*')
    Driving_licence = models.CharField(max_length=20, choices=driv, default='*')
    Age_appropriateness = models.CharField(max_length=20, choices=ageapr, default='*')
    Disability_appropriateness = models.CharField(max_length=20, choices=disapr, default='*')
    SKP_Wish = models.CharField(max_length=20, choices=skpwish, default='*')
    BO_wishes_for_contract_type = models.CharField(max_length=20, choices=bowishct, default='*')
    Job_contract_type = models.CharField(max_length=20, choices=jobctrtype, default='*')
    BO_career_wishes = models.CharField(max_length=20, choices=bocrwish, default='*')
    Job_career_advancement = models.CharField(max_length=20, choices=jobcradv, default='*')
    BO_working_hours_wishes = models.CharField(max_length=20, choices=bowhwish, default='*')
    Job_working_hours = models.CharField(max_length=20, choices=jobwh, default='*')
    MSO = models.CharField(max_length=20, choices=msoo, default='*')
    BO_wish_location = models.CharField(max_length=20, choices=bowishloc, default='*')