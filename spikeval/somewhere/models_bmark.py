from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from tagging.fields import TagField

class Benchmark(models.Model):
    """
    Benchmark is a class representing a set of Benchmark data files, organized 
    in Records. Each Record contains one Groundtruth File with corresponding raw
    benchmark data files (may be several due to different formats). Typically, 
    a whole Benchmark belongs to one scientist.
    """
    BENCHMARK_STATES = (
        ('N', 'New/Non-active'),
        ('A', 'Active'),
        ('C', 'Closed'),
    )
    name = models.CharField(_('name'), blank=True, max_length=200)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, related_name="benchmark owner", blank=True)
    state = models.CharField(max_length=1, default="N", choices=BENCHMARK_STATES)
    tags = TagField(_('keywords'))
    date_created = models.DateTimeField(_('date created'), default=datetime.now, editable=False)
    added_by = models.ForeignKey(User, blank=True, editable=False)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return ("b_details", [self.pk])
    get_absolute_url = models.permalink(get_absolute_url)

    def is_active(self):
        return self.state == "A"

    def is_accessible(self, user):
        return (self.owner == user or self.is_active())

    def archive(self):
        self.state = "C"
        self.save()

    def evaluations(self):
        """
        Returns evaluations related with this Benchmark.
        """
        evals = None
        records = self.record_set.all()
        if records:
            evals = records[0].evaluations()
        for r in records:
            e = r.evaluations()
            if e:
                evals = evals | r.evaluations()
        return evals

    def eval_count(self):
        return len(self.evaluations())

class Record(models.Model):
    """
    A Record is a unique pair of groundtruth - raw data benchmark files, 
    representing a unit, against which users can make evaluations of their 
    algorithms. Actually, there can be several raw data files in the record,
    however they should differ only with the format, not with their contents.
    """
    name = models.CharField(_('name'), blank=True, max_length=200)
    description = models.TextField(blank=True, null=True)
    benchmark = models.ForeignKey(Benchmark)
    date_created = models.DateTimeField(_('date created'), default=datetime.now, editable=False)
    added_by = models.ForeignKey(User, blank=True, editable=False)

    def get_active_rfile(self):
        try:
            r = self.datafile_set.filter(filetype="R")[0]
        except IndexError:
            r = "#"
        return r

    def get_active_gfile(self):
        try:
            r = self.datafile_set.filter(filetype="G")[0]
        except IndexError:
            r = "#"
        return r

    def evaluations(self):
        """
        Returns evaluations related to this Record.
        """
        evals = None
        datafiles = self.datafile_set.filter(filetype="R")
        if datafiles:
            evals = datafiles[0].evaluations()
        for f in datafiles:
            e = f.evaluations()
            if e:
                evals = evals | f.evaluations()
        return evals

    def eval_count(self):
        return len(self.evaluations())
