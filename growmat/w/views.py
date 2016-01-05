from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
#from django.template.context import RequestContext
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone

 
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Instrument
from .models import InstrumentForm
#from .models import InstrumentList

from .models import Rule
from .models import RuleForm

from .models import Period
from .models import PeriodForm

from .models import Archive

import shutil
import os
import fnmatch
import math

import os, tempfile, zipfile, time
#from django.core.servers.basehttp import FileWrapper
from django.conf import settings
import mimetypes

#from test.utils import instrumented_test_render

# coding: utf-8

from django.contrib import auth






class InstrumentCreate(CreateView):
    model = Instrument
    fields = ['address', 'type', 'index', 'name']
    #success_url('w')
    def get_success_url(self):
        return reverse('w:list')

class InstrumentUpdate(UpdateView):
    model = Instrument
    fields = ['address', 'type', 'index', 'name']
    def get_success_url(self):
        return reverse('w:list')


class InstrumentDelete(DeleteView):
    model = Instrument
    success_url = reverse_lazy('w:instrument/0')   

class RuleDelete(DeleteView):
    model = Rule
    success_url = reverse_lazy('w:rule/0')   

class PeriodDelete(DeleteView):
    model = Period
    success_url = reverse_lazy('w:period/0')

PROJECT_PATH = os.path.dirname(settings.BASE_DIR)
# Create your views here.
def save(request):
    os.system('sync')
    
    os.path.join(PROJECT_PATH,'growmat', 'ramdisk', 'db.sqlite3')
    shutil.copy2( os.path.join(PROJECT_PATH,'growmat', 'ramdisk', 'db.sqlite3'),  os.path.join(PROJECT_PATH, 'db.sqlite3') )
    #shutil.copy2('/home/pi/growmat/growmat/ramdisk/db.sqlite3', '/home/pi/growmat/db.sqlite3' )
    
    context = RequestContext(request, {
            'message': 'Database saved!' })
    
    return render(request, 'w/message.html', context)

def archive(request, pk=0):
    
    #os.system('/home/pi/growmat/garchive')
    import management.commands.archive
    
    management.commands.archive.appendArchives()
    
    #path = '/home/pi/growmat/archives/' + str(pk) 
    path = os.path.join(PROJECT_PATH,'growmat', 'archives', str(pk), '')
    print path
    #if pk is None:
    #    pk = '*'
    
    f = []
    for file in os.listdir(path):
        if fnmatch.fnmatch(file, '*-' + str(pk) + '.csv'):
            f.append(file)
            #print file

    context = RequestContext(request, {
            'archives': f })
    
    return render(request, 'w/archive.html', context)
    
    
    os.system('/home/pi/growmat/garchive')

    filename     = '/home/pi/growmat/archives/'+ str(pk) + '.csv'
    download_name = str(pk)  + '.csv'
    wrapper      = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response     = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] ='attachment; filename=%s'%download_name
    return response
  
    return render(request, 'w/archive_csv.html')
    
    
    
    if pk:
        instrument0 = Instrument.objects.get(pk=pk)
        archives = Archive.objects.filter(instrument=instrument0).order_by('datetime')
    else:
        archives = Archive.objects.order_by('datetime', 'instrument')
    
    context = RequestContext(request, {
        'archives': archives
    })

    return render(request, 'w/archive.html', context)
   

def webcam(request, pk='0'):
    #path = os.path.join(PROJECT_PATH,'growmat','ramdisk', 'fswebcam.jpg')
    #os.system('raspistill -w 640 -h 480 -vf  -n -t 0 -o ' + path) #-tl 60000
    filename = str(pk) + '.jpg'
    pathDst = os.path.join(PROJECT_PATH,'growmat','ramdisk', filename)
    
    if pk == '0':
        os.system('pkill -SIGUSR1 raspistill')
        pathSrc = os.path.join(PROJECT_PATH,'growmat','ramdisk', 'raspistill.jpg')
    
        os.system('cp -f ' + pathSrc + ' ' + pathDst)
    
    text = time.ctime(os.path.getmtime(pathDst))
    context = RequestContext(request, {
            'filename': filename,
            'text': text,
             })
    return render(request, 'w/webcam.html', context)

def index(request, page=0):
    page = int(page)
    instrumentsOnPage = 20
    
    username = 'local'
    password =  'local'
    #if authuser.username != username:
    host = request.get_host()
    if 'localhost' in host:
        authuser = auth.authenticate(username=username, password=password)
        auth.login(request, authuser)
        #print authuser.username
        
    
    instruments = Instrument.objects.order_by('priority')
    lastpage = int(math.ceil(len(instruments)/instrumentsOnPage))
    instruments = instruments[page*instrumentsOnPage:page*instrumentsOnPage+instrumentsOnPage]
    
    nextpage = page + 1
    nextpage = min(nextpage, lastpage)
    
    prevpage = page - 1
    prevpage = max(prevpage, 0)
    
    context = RequestContext(request, {
            'instruments': instruments,
            'page' : page,
            'lastpage' : lastpage,
            'nextpage' : nextpage ,
            'prevpage' : prevpage  })
    return render(request, 'w/index.html', context)        

def detail(request, page=0, pk=None):
    instrument = Instrument.objects.get(pk=pk)
    if request.method == 'POST':
        if 'resetManual' in request.POST:
            instrument.manual = False
            #instrument.status = instrument.status | 1
            instrument.save()
        else:
        
            form = InstrumentForm(request.POST)
            value = instrument.value
            if 'setValue' in request.POST:
                value = form.data['value']
                #if form.is_valid():
                #    data = form.cleaned_data
                #    value = data['value']
                #else:
                #    value = form['value'].value()
                #value = form.data['value']
                #x =  form.data
            if 'setOff' in request.POST:
                value = 0
            if 'setOn' in request.POST:
                value = 1
            instrument.value = value
            instrument.datetime = timezone.now()
            instrument.status = 0 #instrument.status & ~ 3
            instrument.manual = True
            instrument.save()        
        return HttpResponseRedirect('/w/' + page)
    
    #instrument = Instrument.objects.get(pk=pk)
    form = InstrumentForm(instance = instrument)
    context = RequestContext(request, {
        'instrument': instrument,
        'form':form,
        'page': page })
    return render(request, 'w/detail.html', context)
	
def instrument(request, pk=None):
    form = InstrumentForm()

   
    if request.method == 'POST':
        if 'create' in request.POST:
        #if int(pk)==0:
            form = InstrumentForm(request.POST)
            #form = InstrumentForm(request.POST, instance=instrument)
            #form.value = 0.0
            #form.status = 1
            if form.is_valid():
                form.save()
            #print form.is_valid()
                return HttpResponseRedirect('/w/instrument/')
            form.pk = 0
            instruments = Instrument.objects.order_by('pk')    
            context = RequestContext(request, {
                'instruments': instruments, 'form':form
            })
            return render(request, 'w/instrument.html', context)

        #else:
        if 'save' in request.POST:
            #print pk
            instrument = Instrument.objects.get(pk=pk)
            form = InstrumentForm(request.POST, instance = instrument)
            #form.value = 0.0
            #form.status = 1
            if form.is_valid():
                #print 'update'
                form.save()
                #print form.is_valid()
                return HttpResponseRedirect('/w/instrument')
            
            form.pk = pk
            instruments = Instrument.objects.order_by('pk')    
            context = RequestContext(request, {
                'instruments': instruments, 'form':form
            })
            return render(request, 'w/instrument.html', context)


                
        if 'delete' in request.POST:
            #print pk
            instrument = Instrument.objects.get(pk=pk)
            instrument.delete()
            pk=0
            return HttpResponseRedirect('/w/instrument')
    
    else:
        instruments = Instrument.objects.order_by('pk')
        if pk:
            if int(pk)== 0:
                form = InstrumentForm()
                form.pk=0
                context = RequestContext(request, {
                    'instruments': instruments, 'form':form })
                return render(request, 'w/instrument.html', context)
            
            if int(pk)>0:
                #print pk
                instrument = Instrument.objects.get(pk=pk)
                form = InstrumentForm(instance = instrument)
            
                form.pk=int(pk)
                context = RequestContext(request, {
                    'instruments': instruments, 'form':form })
                return render(request, 'w/instrument.html', context)

        context = RequestContext(request, {
            'instruments': instruments })
        return render(request, 'w/instrument.html', context)           
		
        
        
# Create your views here.
def rule(request, pk=None):
    form = RuleForm()
   
    if request.method == 'POST':
        if 'create' in request.POST:
            form = RuleForm(request.POST)
            if form.is_valid():
                form.save()
            #print form.errors
                return HttpResponseRedirect('/w/rule/')
            
            form.pk = 0
            rules = Rule.objects.order_by('priority')    
            context = RequestContext(request, {
                'rules': rules, 'form':form
            })
            return render(request, 'w/rule.html', context)
    
        if 'save' in request.POST:
            rule = Rule.objects.get(pk=pk)
            form = RuleForm(request.POST, instance = rule)
            if form.is_valid():
                form.save()

                return HttpResponseRedirect('/w/rule/')
            form.pk = pk
            rules = Rule.objects.order_by('priority')    
            context = RequestContext(request, {
                'rules': rules, 'form':form
            })
            return render(request, 'w/rule.html', context)
                
        if 'delete' in request.POST:
            rule = Rule.objects.get(pk=pk)
            rule.delete()
            return HttpResponseRedirect('/w/rule/')
        
    else:
        rules = Rule.objects.order_by('priority')
        
        if pk:
            if int(pk)>0:
                rule = Rule.objects.get(pk=pk)
                form = RuleForm(instance = rule)
            
                form.pk=int(pk)
                
                context = RequestContext(request, {
                    'rules': rules,  'form':form
                })

                return render(request, 'w/rule.html', context)
             
            if int(pk)==0: 
                form = RuleForm() 
                form.pk = 0
                context = RequestContext(request, {
                    'rules': rules,  'form':form
                })

                return render(request, 'w/rule.html', context) 

        context = RequestContext(request, {
                    'rules': rules
                })

        return render(request, 'w/rule.html', context) 
                
    rules = Rule.objects.order_by('pk')
    
    #for object in objects:
    #    object.fields = dict((field.name, field.value_to_string(object))
    #    for field in object._meta.fields)

    
    #context = RequestContext(request, {
    #    'instruments': instruments, 'list':list, 'form0':form0, 'form':form
    #})
    context = RequestContext(request, {
        'rules': rules, 'form':form
    })

    return render(request, 'w/rule.html', context)

        

	
#	output = ', '.join([p.user_name for p in instrument_list])
#	return HttpResponse(output)

def instrumentAdd(request):
	#if 'addTemperature' in request.POST:
		#instrument = InstrumentTemperature.objects.create()
	#	instrument = InstrumentTemperature.objects.create()
		#instrument = Instrument()
		#form = InstrumentTemperatureForm()
		#return render(request, 'w/instrument.html', {'form': form})	#return render(request, 'w/instrument.html', {'form': form})
		#return render(request, 'w/instrument.html', {'form': form, 'instrument': instrument})
	#return HttpResponseRedirect('/w')
	instrument = Instrument(pk=0)
	#form = InstrumentForm()
	form = InstrumentCreate()
	return render(request, 'w/instrument.html', {'form': form, 'instrument': instrument})
	
def instrumentXXX(request, instrument_id):
	
	if int(instrument_id)>0:
		instrument = Instrument.objects.get(pk=instrument_id)
		
	
	#try:
	#	a = InstrumentTemperature.objects.get(pk=instrument_id)
	#except InstrumentTemperature.DoesNotExist:
	#	a = Instrument.objects.get(pk=instrument_id)
			
	if request.method == 'POST':
		#if 'addTemperature' in request.POST:
		#	form = InstrumentTemperatureForm()
			#return render(request, 'w/instrument.html', {'form': form})
	
		#try:
		#	a = InstrumentTemperature.objects.get(pk=instrument_id)
		#except InstrumentTemperature.DoesNotExist:
		#	a = Instrument.objects.get(pk=instrument_id)
		
		#print 'ssfsf' 
		#a = Instrument.objects.get(pk=instrument_id)
		#print isinstance(a, InstrumentTemperature)
		#print a.self
		#print type(a).__name__
		if 'delete' in request.POST:
			instrument.delete()
			return HttpResponseRedirect('/w')
			#return render(request, 'w/index.html')				return HttpResponseRedirect('/w')
			# create a form instance and populate it with data from the request
		
			
			#a.delete()
		if 'copy' in request.POST:
			form = InstrumentForm(request.POST)
		
		if 'save'in request.POST:
			
			if int(instrument_id)>0:
				form = InstrumentForm(request.POST, instance=instrument)
			else:
				form = InstrumentForm(request.POST)
			
					
		# check whether it's valid:
		#print 'XXXd2'
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			#return HttpResponseRedirect(reverse('w:instrument', args=(instrument.id,)))
			#print form.fields['user_name'].value
			#form.save(commit=False)
			
			saved_instrument = form.save()
			
			instrument = get_object_or_404(Instrument, pk=saved_instrument.pk)
			
			#+--	print 'fdfdfdf'#instrument=(InstrumentTemperature)instrument
			#return HttpResponseRedirect('/')
			
			#instrument = get_object_or_404(Instrument, pk=instrument_id)
			#print '!!!'
			return render(request, 'w/instrument.html', {'form': form, 'instrument': instrument})
		#print 'XXXd3'
		#print form.errors
		return render(request, 'w/instrument.html', {'form': form, 'instrument': instrument})
	# if a GET (or any other method) we'll create a blank form
	else:
		#instrument = get_object_or_404(Instrument, pk=instrument_id)		
			
		#try:
		#	instrument = InstrumentTemperature.objects.get(pk=instrument_id)	
		#except InstrumentTemperature.DoesNotExist:
		#	instrument = get_object_or_404(Instrument, pk=instrument_id)	
		
		#try:
		#	instrument2 = Instrument.objects.get(instrument_id=instrument.id)
		#except:
		#	instrument2 = None
		#if isinstance(instrument, InstrumentTemperature):
		#	form = InstrumentTemperatureForm(instance = instrument)
		#else:
		#form = InstrumentForm(instance = instrument)
		#form = InstrumentForm(instance = insrument2)
		
		form = InstrumentForm(instance = instrument)
		return render(request, 'w/instrument.html', {'form': form, 'instrument': instrument})
        
        
# Create your views here.
def period(request, pk=None):
    form = PeriodForm()
   
    if request.method == 'POST':
        if 'create' in request.POST:
            form = PeriodForm(request.POST)
            if form.is_valid():
                form.save()
            #print form.errors
                return HttpResponseRedirect('/w/period/')
            
            form.pk = 0
            periods = Period.objects.order_by('pk')    
            context = RequestContext(request, {
                'periods': periods, 'form':form
            })
            return render(request, 'w/period.html', context)
    
        if 'save' in request.POST:
            period = Period.objects.get(pk=pk)
            form = PeriodForm(request.POST, instance = period)
            if form.is_valid():
                form.save()

                return HttpResponseRedirect('/w/period/')
            form.pk = pk
            periods = Period.objects.order_by('pk')    
            context = RequestContext(request, {
                'periods': periods, 'form':form
            })
            return render(request, 'w/period.html', context)
                
        if 'delete' in request.POST:
            period = Period.objects.get(pk=pk)
            period.delete()
            return HttpResponseRedirect('/w/period/')
        
    else:
        periods = Period.objects.order_by('pk')
        
        if pk:
            if int(pk)>0:
                period = Period.objects.get(pk=pk)
                form = PeriodForm(instance = period)
            
                form.pk=int(pk)
                
                context = RequestContext(request, {
                    'periods': periods,  'form':form
                })

                return render(request, 'w/period.html', context)
             
            if int(pk)==0: 
                form = PeriodForm() 
                form.pk = 0
                context = RequestContext(request, {
                    'periods': periods,  'form':form
                })

                return render(request, 'w/period.html', context) 

        context = RequestContext(request, {
                    'periods': periods
                })

        return render(request, 'w/period.html', context) 
                
    periods = Period.objects.order_by('pk')
    
    context = RequestContext(request, {
        'periods': periods, 'form':form
    })

    return render(request, 'w/period.html', context)

