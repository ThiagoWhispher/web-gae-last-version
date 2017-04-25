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
        self.render("index.html")

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
        disciplinas = Disciplina.query()
        cursos = Curso.query()
        curso = self.request.get('key')
        self.render("disciplina.html", disciplinas=disciplinas, cursos=cursos, Curso=Curso, curso=curso)

    def post(self):
        #a fazer
        #definir variavel para os ids dos cursos
        nome   = self.request.get("nome")
        periodo  = self.request.get("periodo")
        periodo = int(periodo)
        curso = self.request.get("curso")
        curso=int(curso)

        disciplina = Disciplina(nome=nome, periodo=periodo, curso=curso)
        disciplina.put()
        time.sleep(.1)

        key = self.request.get("key")
        self.redirect(key)

class DeleteHandler(webapp2.RequestHandler):
    def get(self):
        key = ndb.Key(urlsafe=self.request.get('id'))
        key.delete()
        time.sleep(.1)
        if(self.request.get('page') == 'professor'):
            self.redirect('/professor')
        elif(self.request.get('page') == 'curso'):
            self.redirect('/curso')
        else:
            params = {'key': ''}
            r = requests.get('/disciplina', params=params)
            self.redirect(r.url)

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
        self.redirect("/curso")

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
        cursos=Curso.query()
        self.render("editar_disciplina.html", disciplina=disciplina, cursos=cursos)
    
    def post(self):
        key = ndb.Key(urlsafe=self.request.get('key'))
        disciplina = key.get()
        disciplina.nome   = self.request.get('nome')
        periodo   = self.request.get('periodo')
        disciplina.periodo = int(periodo)
        curso   = self.request.get('curso')
        disciplina.curso=int(curso)
        disciplina.put()
        time.sleep(.1)
        self.redirect("/disciplina")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/professor', ProfessorHandler),
    ('/curso', CursoHandler),
    ('/disciplina', DisciplinaHandler),
    ('/img', ImageHandler),
    ('/updatecurso', UpdateCursoHandler),
    ('/updateprofessor', UpdateProfessorHandler),
    ('/updatedisciplina', UpdateDisciplinaHandler),
    ('/delete', DeleteHandler)
], debug=True)