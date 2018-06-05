# Copyright (C) 2017 Savoir-faire Linux Inc. (<www.savoirfairelinux.com>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=75)
    password = models.CharField(max_length=75)
    email = models.CharField(max_length=75)


    def __repr__(self):
        return '<User: %s>' % self.name

    def __str__(self):
        return self.name



class Compentency(models.Model):
    name = models.CharField(max_length=75)
    interest = models.IntegerField  # 1: low interest, 4: high interest

    def __repr__(self):
        return '<Compentency: %s>' % (self.name)

    def __str__(self):
        return self.name
