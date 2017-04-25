# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, invalid-name, import-error

from google.appengine.ext import ndb

class Professor(ndb.Model):
    nome = ndb.StringProperty(required=True)
    area = ndb.StringProperty(required=True)
    perfil = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    foto = ndb.BlobProperty()

class Curso(ndb.Model):
	nome = ndb.StringProperty(required=True)
	periodos = ndb.StringProperty(required=True)
	semestral = ndb.StringProperty(required=True)

class Disciplina(ndb.Model):
	nome = ndb.StringProperty(required=True)
	periodo = ndb.IntegerProperty(required=True)
	curso = ndb.IntegerProperty(required=True)
