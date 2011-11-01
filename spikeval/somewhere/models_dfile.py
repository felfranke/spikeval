from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.files import storage
from django.core.exceptions import MultipleObjectsReturned
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from benchmarks.models import Record

def make_upload_path(self, filename):
    """
    Generates upload path for FileField.
    """
    return "data/%s/%s" % (self.owner.username, filename)


class FileSystemStorage(storage.FileSystemStorage):
    """
    Subclass Django's standard FileSystemStorage to fix permissions
    of uploaded files.
    """

    def _save(self, name, content):
        name = super(FileSystemStorage, self)._save(name, content)
        full_path = self.path(name)
        mode = getattr(settings, 'FILE_UPLOAD_PERMISSIONS', None)
        if not mode:
            mode = 0644
        os.chmod(full_path, mode)
        return name


class Datafile(models.Model):
    """
    Datafile is a class representing a data file stored at G-Node.
    """
    FILETYPE_CHOICES = (
        ('R', 'Raw Benchmark Data File'),
        ('G', 'Groundtruth Benchmark File'),
        ('U', 'User Uploaded File'),
        )
    filetype = models.CharField(max_length=1, choices=FILETYPE_CHOICES)
    record = models.ForeignKey(Record, blank=True)
    date_created = models.DateTimeField(_('date created'),
                                        default=datetime.now
                                        , editable=False)
    added_by = models.ForeignKey(User, blank=True, editable=False)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return ("download", [self.pk])

    get_absolute_url = models.permalink(get_absolute_url)

    def get_version(self, version=None):
        """
        Returns the requested version of the file. Returns last version, if
        the version number is omitted.
        """
        try:
            if version:
                v = self.version_set.filter(version=version)[0]
            else:
                v = self.version_set.order_by("-version")[0]
        except MultipleObjectsReturned:
            v = None
        return v

    def get_next_version_index(self):
        """
        Provides the next index for the new file version.
        """
        return self.version_set.all().count() + 1

    def is_accessible(self, user):
        """
        Depending on the state of the parent benchmark and the file ownership,
        this function defines, who may see the file.
        """
        b = self.record.benchmark
        return (b.owner == user or (b.is_active() and self.filetype == "R"))

    def evaluations(self):
        """
        Returns evaluations related to this Datafile.
        """
        evals = None
        versions = self.version_set.all()
        if versions:
            evals = versions[0].evaluations()
        for v in versions:
            e = v.evaluations()
            if e:
                evals = evals | v.evaluations()
        return evals

    @property
    def name(self):
        lv = self.get_version()
        return lv.title

    @property
    def size(self):
        return self.get_version().size


class Version(models.Model):
    """
    Implements versioning for datafiles.
    """
    title = models.CharField(_('title'), max_length=200)
    version = models.IntegerField()
    datafile = models.ForeignKey(Datafile)
    raw_file = models.FileField(_('data file'),
                                upload_to="files/benchmarks/") # or
                                # make_upload_path.. which doesn't work for
                                # Python 2.5
    date_created = models.DateTimeField(_('date created'),
                                        default=datetime.now
                                        , editable=False)
    added_by = models.ForeignKey(User, blank=True, editable=False)

    def evaluations(self):
        """
        Returns evaluations related to a specific Version.
        """
        return self.evaluation_set.all()

    def get_absolute_url(self):
        return ("download", [self.pk, self.version])

    get_absolute_url = models.permalink(get_absolute_url)

    @property
    def size(self):
        return filesizeformat(self.raw_file.size)

