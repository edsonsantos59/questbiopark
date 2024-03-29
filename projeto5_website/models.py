from django.db import models
import uuid
from django.utils.text import slugify  
class GeeksModel(models.Model): 
    title = models.CharField(max_length = 200) 
    slug = models.SlugField() 

    def save(self, *args, **kwargs): 
      maior = self.dominancia
      self.resultado_final = 'dominancia'
      if self.cautela > maior:
        maior = self.cautela
        self.resultado_final = 'cautela'
      if self.influencia > maior:
        maior = self.influencia
        self.resultado_final = 'influencia'
      if self.estabilidade > maior:
        maior = self.estabilidade
        self.resultado_final = 'estabilidade'
      super(Resultado, self).save(*args, **kwargs)

class Turma(models.Model):
  curso = models.CharField(max_length=50)
  ano = models.IntegerField()
  semestre = models.IntegerField() #TODO:


class Aluno(models.Model):
  nome = models.CharField(max_length=30)
  ra = models.IntegerField(unique=True, blank=False)
  email = models.EmailField(max_length=254, blank=False)
  #turma = models.ManyToManyField(Turma)
  def __str__(self):
      return str(self.ra)

class Resultado(models.Model):
  aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
  data_ini = models.DateTimeField()
  data_fim = models.DateTimeField()
  influencia = models.FloatField()
  dominancia = models.FloatField()
  cautela = models.FloatField()
  estabilidade = models.FloatField()
  resultado_final = models.CharField(max_length=50)

  def get_resultado_final(self):
    res_perfis = [("Dominante", self.dominancia), 
                  ("Influente",self.influencia), 
                  ("Cauteloso",self.cautela), 
                  ("Estável",self.estabilidade)]
    res_perfis.sort(reverse=True, key=lambda t: t[1])
    res = ""
    for perfil in res_perfis:  
      if perfil[1] == res_perfis[0][1]:
        res += perfil[0] + ' '
    return res

  def save(self, *args, **kwargs): 
    self.resultado_final = self.get_resultado_final()
    super(Resultado, self).save(*args, **kwargs)
  
  def __str__(self):
      return ' - '.join([str(self.aluno.ra)])

class Teste(models.Model):
  nome = models.CharField(max_length=30)

  def __str__(self):
    return self.nome

class Pergunta(models.Model):
  teste = models.ForeignKey(Teste, on_delete=models.CASCADE)
  enunciado = models.TextField(max_length=140)
  
  def __str__(self):
    return self.enunciado

CHOICES_ALTERNATIVA = (
  (1,'dominancia'),
  (2,'influencia'),
  (3,'cautela'),
  (4,'estabilidade'),
)

class Alternativa(models.Model):
  pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
  conteudo = models.CharField(max_length=140, blank=False)
  perfil = models.IntegerField(choices=CHOICES_ALTERNATIVA, blank=False)
  
  def __str__(self):
    return ' - '.join([self.conteudo, 
        self.pergunta.__str__()[:15]+'...',
        self.pergunta.teste.__str__()])