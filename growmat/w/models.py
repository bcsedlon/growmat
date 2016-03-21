from django.db import models
from django.forms import ModelForm
from django.views.generic import ListView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse




# Create your models here.
class Instrument(models.Model):
	
	#INI = 1 << 0
	cNT = 1<<0
	cIV = 1<<1
	cA  = 1<<2
	cW  = 1<<3
	
	INSTRUMENT_TYPE = (
					(0, 'SYSTEM'),
					(10, 'OUTPUT'),
     				(20, 'THERMOMETER'),
         			(30, 'HUMIDITYMETER'),
    			    (40, 'DISTANCEMETER'),
    				(50, 'PHMETER'),    				
	)
	
	INSTRUMENT_INDEX = (
					(0, '0'),
     				(1, '1'),
         			(2, '2'),
    			    (3, '3'),
    				(4, '4'),
    				(5, '5'),
     				(6, '6'),
         			(7, '7'),
    			    (8, '8'),
    				(9, '9'),
	)
	
	DATA_TYPE = (
					(0, 'int'),
     				(1, 'float'),
	)
	
		
	priority = models.FloatField(default=0, blank=True)
	manual = models.BooleanField(default=False, blank=True)
	address = models.IntegerField(default=0)
	type = models.IntegerField(choices=INSTRUMENT_TYPE, default=0)
	#index = models.IntegerField(choices=INSTRUMENT_INDEX, default=0)
	index = models.IntegerField(default=0)
	output = models.BooleanField(default = False, blank=True)
	datatype = models.IntegerField(choices=DATA_TYPE, default=0)
	name = models.CharField(default='NEW',  max_length=256)
	value = models.FloatField(default=0)
	status = models.IntegerField(default=1) 
	datetime = models.DateTimeField(null=True, blank=True) 
	
	#def get_absolute_url(self):
	#	return reverse('list', kwargs={'pk': self.pk})
	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in Instrument._meta.fields]
	
	def NT(self):
		return self.status & Instrument.cNT
	def IV(self):
		return self.status & Instrument.cIV
	def A(self):
		return self.status & Instrument.cA
	def W(self):
		return self.status & Instrument.cW
	
	
	
class InstrumentForm(ModelForm):
    class Meta:
        model = Instrument
        fields = ['priority', 'manual', 'address', 'type', 'index', 'output', 'datatype','name', 'value', 'status', 'datetime']


class InstrumentList(ListView):
	model = Instrument
		#queryset = Instrument.objects.all()
		#fields = ['address', 'type', 'index', 'name', 'value', 'status', 'datetime']		
#class Choice(models.Model):
#    question = models.ForeignKey(Question)
#    choice_text = models.CharField(max_length=200)
#    votes = models.IntegerField(default=0)


class Period(models.Model):
	name = models.CharField(default='NEW',  max_length=256)
	time_from = models.TimeField()
	time_to = models.TimeField()
	description = models.CharField(null=True, blank=True,  max_length=256) 
	
	

class PeriodForm(ModelForm):
    class Meta:
        model = Period
        fields = ['name', 'time_from', 'time_to', 'description']	
        


class Rule(models.Model):	

	
	ATTRIBUTE_TYPE = (
					('VALUE', 'VALUE'),
     				('STATUS', 'STATUS'),
         			('NT', 'NT'),
    			    ('IV', 'IV'),
    			    ('W', 'WARNING'),
    			    ('A', 'ALARM'),
	)
	
	OPERATION_TYPE = (
					('<', '<'),
					('<=', '<='),
     				('==', '=='),
         			('>', '>'),
         			('>=', '>='),
    			    ('!=', '!='),
    			    ('and', 'AND'),
    			    ('or', 'OR'),
	)
	
	ACTION_TYPE = (
					('None', 'None'),
					('=', '='),
					('&', '&'),
					('& ~', '& ~'),
					('|', '|'),
					('| ~', '| ~'),
					('+', '+'),
					('-', '-'),
					('*', '*'),
					('/', '/'),
					('%', '%'),
	)
	
	priority = models.FloatField(default=0, blank=True)
	period = models.ForeignKey(Period)
	input = models.ForeignKey(Instrument, related_name='input_instrument')
	input_attribute = models.CharField(choices=ATTRIBUTE_TYPE, default=0, max_length=6)
	input_operation = models.CharField(choices=OPERATION_TYPE, default=0, max_length=2)
	input_parameter = models.FloatField(default=0, blank=True)
	output = models.ForeignKey(Instrument, related_name='output_instrument')
	output_attribute = models.CharField(choices=ATTRIBUTE_TYPE, default=0, max_length=6)
	output_action_true = models.CharField(choices=ACTION_TYPE, default='None', max_length=4)
	output_parameter_true = models.FloatField(default=0, blank=True)
	output_action_false = models.CharField(choices=ACTION_TYPE, default='None', max_length=4)
	output_parameter_false = models.FloatField(default=0, blank=True)
	description = models.CharField(null=True, blank=True,  max_length=256) 
	result = models.BooleanField(default=False, blank=True) 
	result0 = models.BooleanField(default=False, blank=True) 
	datetime = models.DateTimeField(null=True, blank=True) 
	once = models.BooleanField(default=False, blank=True) 

class RuleForm(ModelForm):
    class Meta:
        model = Rule
        fields = ['priority', 'period', 'input', 'input_attribute', 'input_operation', 'input_parameter', 'output', 'output_attribute', 'output_action_true', 'output_parameter_true', 'output_action_false', 'output_parameter_false', 'description', 'result', 'result0', 'datetime', 'once']
        
    def __init__(self, *args, **kwargs):
        super(RuleForm, self).__init__(*args, **kwargs)
        self.fields['input'].queryset = Instrument.objects.all()
        self.fields['input'].label_from_instance = lambda obj: "%s" % (obj.name)
        self.fields['output'].queryset = Instrument.objects.all()
        self.fields['output'].label_from_instance = lambda obj: "%s" % (obj.name)
        
        self.fields['period'].queryset = Period.objects.all()
        self.fields['period'].label_from_instance = lambda obj: "%s" % (obj.name)
        
        
class Archive(models.Model):	
	instrument = models.ForeignKey(Instrument)
	value = models.FloatField(default=0, null=True, blank=True)
	status = models.IntegerField(default=0, null=True, blank=True)
	datetime = models.DateTimeField(null=True, blank=True) 
	

	
	
	 

	