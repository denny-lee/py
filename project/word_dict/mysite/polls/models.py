# from django.db import models
from datetime import datetime

# Create your models here.


class BaseModel(dict):
    _id = None
    created_at = None
    updated_at = None

    def __str__(self):
        return "base model"

    def get_coll(self):
        return "Raw_data"

    def checkRequired(self):
        return True

    def set_dates(self, dt=datetime.now()):
        self.created_at = dt
        self.updated_at = dt

    def update_dt(self, dt=datetime.now()):
        self.updated_at = dt


class EngBook(BaseModel):
    expr = None     # R     indexed
    expr_type = None
    phonetic_symbol = None
    trans = None    # R
    subject = None  # R
    branch = None
    synonym = None              # comma separated string
    similar_spelling = None     # comma separated string
    tag = None
    example = None
    search_count = None

    def __init__(self, expr=None, trans=None, subject=None, tag=None, example=None, synonym=None, similar_spelling=None):
        self.expr = expr
        self.trans = trans
        self.subject = subject
        self.tag = tag
        self.example = example
        self.synonym = synonym
        self.similar_spelling = similar_spelling

    def __str__(self):
        return "Eng Word Book"

    def get_coll(self):
        return "eng_book"

    def checkRequired(self):
        if not self.expr or not self.trans or not self.subject:
            return False
        return True

    def merge(self, obj):
        self._id = obj['_id']
        self.expr = obj['expr']
        self.trans = obj['trans']
        self.subject = obj['subject']
        if 'expr_type' in obj:
            self.expr_type = obj['expr_type']
        if 'phonetic_symbol' in obj:
            self.phonetic_symbol = obj['phonetic_symbol']
        if 'branch' in obj:
            self.branch = obj['branch']
        if 'search_count' in obj:
            self.search_count = obj['search_count']
        if 'example' in obj and self.example is None:
            self.example = obj['example']
        if self.tag is None:
            self.tag = obj['tag']
        elif 'tag' in obj:
            self.merge_tag(obj['tag'])

    def merge_tag(self, tag):
        if self.tag is not None and tag is not None:
            arr = tag.split(',')
            arr_new = self.tag.split(',')
            tag_new = None
            for e in arr_new:
                et = e.strip()
                if arr.index(et) < 0:
                    tag_new += et + ','
            if tag_new is not None:
                if len(tag_new) > 0:
                    tag_new = tag_new[:-1]
                tag_new += ',' + ','.join(arr_new)
                self.tag = tag_new
        elif self.tag is not None:
            self.tag = self.remove_dup_str(self.tag)
        elif tag is not None:
            self.tag = tag

    def remove_dup_str(self, str):
        if str is not None:
            arr = str.split(',')
            arr_n = []
            for e in arr:
                et = e.strip()
                if arr_n.index(et) < 0:
                    arr_n.append(et)
            return ','.join(arr_n)
        return None

class Subject(BaseModel):
    eng_name = None

    def __init__(self, eng_name=None):
        self.eng_name = eng_name

    def __str__(self):
        return self.eng_name

    def get_coll(self):
        return 'subject'

    def checkRequired(self):
        if not self.eng_name:
            return False
        return True
