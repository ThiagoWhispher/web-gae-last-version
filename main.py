# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, invalid-name, import-error

import os
import jinja2
import webapp2
import time

from google.appengine.api import images
from google.appengine.ext import ndb

from model import Professor
from model import Curso
from model import Disciplina

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class ImageHandler(webapp2.RequestHandler):
    def get(self):
        professor_key = ndb.Key(urlsafe=self.request.get('img_id'))
        professor = professor_key.get()
        if professor.foto:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(professor.foto)
        else:
            self.response.out.write('No image')

class MainHandler(Handler):
    def get(self):
        self.write("Olá Mundo!")

class ProfessorHandler(Handler):
    def get(self):
        professores = Professor.query()

        self.render("professor.html", professores=professores)

    def post(self):
        nome   = self.request.get("nome")
        area   = self.request.get("area")
        perfil = self.request.get("perfil")
        email  = self.request.get("email")
        foto   = self.request.get("img")

        professor = Professor(nome=nome, area=area, perfil=perfil,
                              email=email, foto=foto)
        professor.put()
        time.sleep(.1)
        self.redirect('/professor')

class CursoHandler(Handler):
    def get(self):
        cursos = Curso.query()
        self.render("curso.html", cursos=cursos)
    def post(self):
        nome   = self.request.get("nome")
        periodos  = self.request.get("periodos")
        semestral = self.request.get("semestral")

        curso = Curso(nome=nome, periodos=periodos, semestral=semestral)
        curso.put()
        time.sleep(.1)
        self.redirect('/curso')

class DisciplinaHandler(Handler):
    def get(self):
        key_curso = ndb.Key(urlsafe=self.request.get('key'))
        disciplinas = Disciplina.query(Disciplina.curso == key_curso)
        self.render("disciplina.html", disciplinas=disciplinas, key_curso=key_curso)
    def post(self):
        
        nome   = self.request.get("nome")
        periodo  = int(self.request.get("periodo"))
        key_curso = ndb.Key(urlsafe=self.request.get('key'))
        curso = key_curso
        disciplina = Disciplina(nome=nome, periodo=periodo, curso=curso)
        disciplina.put()
        time.sleep(.1)
        self.redirect('/disciplina?key=' + key_curso.urlsafe())


class UpdateCursoHandler(Handler):
    def get(self):
        key = ndb.Key(urlsafe=self.request.get('key'))
        curso = key.get()
        self.render("editar_curso.html", curso=curso)
    
    def post(self):
        key = ndb.Key(urlsafe=self.request.get('key'))
        curso = key.get()
        curso.nome = self.request.get('nome')
        curso.periodos = self.request.get('periodos')
        curso.semestral = self.request.get('semestral')
        curso.put()
        time.sleep(.1)
        self.redirect('/curso')

class UpdateProfessorHandler(Handler):
    def get(self):
        key = ndb.Key(urlsafe=self.request.get('key'))
        professor = key.get()
        self.render("editar_professor.html", professor=professor)
    
    def post(self):
        key = ndb.Key(urlsafe=self.request.get('key'))
        professor = key.get()
        professor.nome   = self.request.get('nome')
        professor.area   = self.request.get('area')
        professor.perfil = self.request.get('perfil')
        professor.email  = self.request.get('email')
        professor.put()
        time.sleep(.1)
        self.redirect("/professor")

class UpdateDisciplinaHandler(Handler):
    def get(self):
        key = ndb.Key(urlsafe=self.request.get('key'))
        disciplina = key.get()
        self.render("editar_disciplina.html", disciplina=disciplina)
    
    def post(self):
        key = ndb.Key(urlsafe=self.request.get('key'))
        disciplina = key.get()
        disciplina.nome   = self.request.get('nome')
        periodo   = self.request.get('periodo')
        disciplina.periodo = int(periodo)
        disciplina.put()
        time.sleep(.1)
        self.redirect("/disciplina?key=" + disciplina.curso.urlsafe())

class DeleteProfessorHandler(webapp2.RequestHandler):
    def get(self):
        key = ndb.Key(urlsafe=self.request.get('key'))
        key.delete()
        time.sleep(.1)
        self.redirect('/professor')

class DeleteCursoHandler(webapp2.RequestHandler):
    def get(self):
        key = ndb.Key(urlsafe=self.request.get('key'))
        key.delete()
        time.sleep(.1)
        self.redirect('/curso')

class DeleteDisciplinaHandler(webapp2.RequestHandler):
    def get(self):
        key = ndb.Key(urlsafe=self.request.get('key'))
        key_curso = key.get().curso
        key.delete()
        time.sleep(.1)
        self.redirect("/disciplina?key=" + key_curso.urlsafe())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/professor', ProfessorHandler),
    ('/curso', CursoHandler),
    ('/disciplina', DisciplinaHandler),
    ('/img', ImageHandler),
    ('/updatecurso', UpdateCursoHandler),
    ('/updateprofessor', UpdateProfessorHandler),
    ('/updatedisciplina', UpdateDisciplinaHandler),
    ('/deleteprofessor', DeleteProfessorHandler),
    ('/deletecurso', DeleteCursoHandler),
    ('/deletedisciplina', DeleteDisciplinaHandler)

], debug=True)
