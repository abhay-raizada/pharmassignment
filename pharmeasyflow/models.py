# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=200)

    def get_all_pending_patients(self, patients):
        pending_patients = []
        for patient in patients:
            if self.user.id in patient.get_pending():
                pending_patients.append(patient)
        return pending_patients

    def get_all_approved_patients(self, patients):
        approved_patients = []
        for patient in patients:
            if self.user.id in patient.get_approved():
                approved_patients.append(patient)
        return approved_patients


class Pharmacist(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=200)

    def get_all_pending_patients(self, patients):
        pending_patients = []
        for patient in patients:
            if self.user.id in patient.get_pending():
                pending_patients.append(patient)
        return pending_patients

    def get_all_approved_patients(self, patients):
        approved_patients = []
        for patient in patients:
            if self.user.id in patient.get_approved():
                approved_patients.append(patient)
        return approved_patients


class Patient(models.Model):
    user = models.OneToOneField(User)
    doctors = models.ManyToManyField(Doctor)
    pharmacist = models.ManyToManyField(Pharmacist)
    name = models.CharField(max_length=200)
    approved = models.TextField(null=True, blank=True)
    medical_record = models.CharField(max_length=200, default = "ACIDITY")
    requested_approval = models.TextField(null=True, blank=True)

    def get_approved(self):
        try:
            return json.loads(self.approved)
        except (TypeError, ValueError):
            return []
    def get_pending(self):
        try:
            return json.loads(self.requested_approval)
        except (TypeError, ValueError):
            return []

    def approve_user(self, _user):
        approved_users = self.get_approved()
        pending_users = self.get_pending()
        approved_users.append(int(_user))
        pending_users.remove(int(_user))
        self.approved = json.dumps(approved_users)
        self.requested_approval = json.dumps(pending_users)
        self.save()

    def add_to_pending(self, _user):
        try:
            pending = json.loads(self.requested_approval)
            pending.append(_user.user.id)
        except (ValueError, TypeError):
            pending = [_user.user.id]
        self.requested_approval = json.dumps(pending)
        self.save() 