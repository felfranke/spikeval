from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from dfiles.models import Version
import math


class Evaluation(models.Model):
    """
    When user wants to evaluate the results of his spike sorting work, he 
    creates an evaluation. Physically, an evaluation binds together 
    user-uploaded file with sorted data, an original version of the raw data 
    file and the evaluation results.
    """
    PROCESSING_STATES = (
        (0, 'In Progress'),
        (1, 'Success'),
        (2, 'Failure'),
    )
    PUBLICATION_STATES = (
        (0, 'Private'),
        (1, 'Public'),
    )
    algorithm = models.CharField(max_length=100, null=True)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, related_name="evaluation owner", blank=True)
    processing_state = models.IntegerField(choices=PROCESSING_STATES)
    publication_state = models.IntegerField(choices=PUBLICATION_STATES)
    user_file = models.FileField(_('sorted data'), upload_to="files/user/")
    original_file = models.ForeignKey(Version)
    error = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(_('date created'), default=datetime.now, editable=False)
    added_by = models.ForeignKey(User, blank=True, editable=False)

    def __unicode__(self):
        return self.algorithm

    def get_absolute_url(self):
        return ("e_details", [self.pk])
    get_absolute_url = models.permalink(get_absolute_url)

    def switch(self):
        """
        Switching the publication state back and forth.
        """
        self.publication_state = int(math.fmod(self.publication_state + 1, 2))
        self.save()

    def processed(self):
        return (self.processing_state > 0)

    def is_public(self):
        return (self.publication_state == 1)

    def is_accessible(self, user):
        return (self.owner == user or self.is_public())

    def benchmark(self):
        """
        Returns related Benchmark.
        """
        return self.original_file.datafile.record.benchmark

    def record(self):
        """
        Returns related Benchmark.
        """
        return self.original_file.datafile.record

    def summary(self):
        """
        Summarized data about evaluation.
        """
        if not self.evaluation_set.all():
            return None
        d = []
        er = EvaluationResults.objects.filter(evaluation=self)
        d.append(er.aggregate(Sum("FP")).values()[0])
        sFN = er.aggregate(Sum("FN")).values()[0]
        sFNO = er.aggregate(Sum("FNO")).values()[0]
        d.append(sFN + sFNO)
        d.append(sFN)
        d.append(sFNO)
        sFPAE = er.aggregate(Sum("FPAE")).values()[0]
        sFPAOE = er.aggregate(Sum("FPAOE")).values()[0]
        d.append(sFPAE + sFPAOE)
        d.append(sFPAE)
        d.append(sFPAOE)
        return d


class EvaluationResults(models.Model):
    """
    Class for keeping evaluation results.
    """
    evaluation = models.ForeignKey(Evaluation)
    gt_unit = models.CharField(max_length=10)
    found_unit = models.CharField(max_length=255)
    TP = models.IntegerField()
    TPO = models.IntegerField()
    FPA = models.IntegerField()
    FPAE = models.IntegerField()
    FPAO = models.IntegerField()
    FPAOE = models.IntegerField()
    FN = models.IntegerField()
    FNO = models.IntegerField()
    FP = models.IntegerField()
    KS = models.IntegerField()
    KSO = models.IntegerField()
    FS = models.IntegerField()
    date_created = models.DateTimeField(_('date created'), default=datetime.now, editable=False)

    def display(self):
        """
        Prepares a stack of results to display.
        """
        d = []
        d.append(self.gt_unit)
        d.append(self.found_unit)
        d.append(self.KS)
        d.append(self.KS - self.KSO)
        d.append(self.TP + self.TPO)
        d.append(self.TP)
        d.append(self.TPO)
        d.append(self.FPAE)
        d.append(self.FPAOE)
        d.append(self.FP)
        d.append(self.FPA)
        d.append(self.FPAO)
        d.append(self.FN)
        d.append(self.FNO)
        return d





