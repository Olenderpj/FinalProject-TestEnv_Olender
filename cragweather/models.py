from django.db import models


#Location Model
class locationModel(models.Model):
    location_name = models.CharField(max_length = 100)
    location_web_link = models.CharField(max_length = 1000)
    location_key = models.IntegerField(default = 00000, primary_key=True)

    def __str__(self):
      return self.location_name;

# Climbing Area Model
class cragModel(models.Model):
    crag_name = models.CharField(default = '', max_length = 200)
    crag_link = models.CharField(default='', max_length = 1000)
    crag_lattitude = models.FloatField(default = 0.00, max_length = 25)
    crag_longitude = models.FloatField(default = 0.00, max_length = 25)

    def __str__(self):
      return self.crag_name

# User Accounts
class userAccountModel(models.Model):
    f_name = models.CharField(max_length = 150)
    l_name = models.CharField(max_length = 150)
    address = models.CharField(max_length = 250)
    phone_number = models.CharField(max_length = 30)
    trad_climber = "Trad"
    sport_climber = "Sport"
    ice_climber = "Ice"
    boulderer = "Boulderer"
    gym_climber = "Gym"
  
    climber_type_choices = [(trad_climber, "Trad Climber"),
    (sport_climber, "Sport Climber"),
    (ice_climber, "Ice Climber"),
    (boulderer, "Boulderer"),
    (gym_climber, "Gym Climber")]
    
    climber_type = models.CharField(max_length = 100, 
    choices = climber_type_choices, 
    default = sport_climber)

    def __str__(self):
      return '{} {}'.format(self.f_name, self.l_name)

class weatherModel(models.Model):
    month = models.CharField(default = "", max_length = 2)
    day = models.CharField(default = "", max_length = 2)
    year = models.CharField(default = "", max_length = 4)
    current_temp = models.IntegerField()
    daily_high_temp = models.IntegerField()
    daily_low_temp = models.IntegerField()
    precip_ammount = models.FloatField(max_length = 4)
    

    def __str__(self):
      return 'DATE: {}/{}/{}'.format(self.month, self.day, self.year)
