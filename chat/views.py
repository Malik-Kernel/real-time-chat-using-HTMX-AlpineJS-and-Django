from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
import re
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User
from chat.models import *
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

def redimensioner_image(image_file,largeur, hauteur):
  #ouvrir l'image avec Pillow
  image=Image.open(image_file)
  #redimensionner
  image.thumbnail((largeur,hauteur))
  #sauvegarder l'image redimensioner dans un buffer
  buffer=BytesIO()
  image.save(buffer, format=image.format)
  buffer.seek(0)

  #retourner l'image redimensionner comme un fichier
  return ContentFile(buffer.read(), name=image_file.name)


class Welcom(View):
    
    def get(self, request):
        data={}
        if request.user.is_authenticated:
          data['profile']=request.user.user_profile
        return render(request, "index.html",data)
    
    def post(self,request):
        if request.user.is_authenticated:
          #message='<i class="fas fa-check text-success"></i> Vous etes deja connecter!'
          return redirect("home")
        else:
          pseudo=request.POST['pseudo']
          password=request.POST['password']
          message=""
          if User.objects.filter(username=pseudo).exists():
            user=authenticate(username=pseudo, password=password)
            if user is not None:
              login(request, user)
              message='<i class="fas fa-check text-success"></i> Connexion reussi!'
            else:
              message='<i class="fas fa-exclamation-triangle text-danger"></i> Votre mot de passe est incorrecte!'
          else:
            message='<i class="fas fa-exclamation-triangle text-danger"></i> Vous avez saisi un pseudo incorrect!'
        if request.user.is_authenticated:
          reponse="""
          <script>
              Swal.fire({
                    title: 'Info!',
                    allowOutsideClick:false,
                    html:'%s',
                    confirmButtonText:'Suivant',
                    showClass: {
                      popup: `
                        animate__animated
                        animate__fadeInUp
                        animate__faster
                      `
                    },
                    hideClass: {
                      popup: `
                        animate__animated
                        animate__fadeOutDown
                        animate__faster
                      `
                    }
                  }).then((result) => {window.location=''});
          </script>
          """%message
        else:
          reponse="""
          <script>
              Swal.fire({
                    title: 'Info!',
                    html:'%s',
                    confirmButtonText:'Daccord',
                    showClass: {
                      popup: `
                        animate__animated
                        animate__fadeInUp
                        animate__faster
                      `
                    },
                    hideClass: {
                      popup: `
                        animate__animated
                        animate__fadeOutDown
                        animate__faster
                      `
                    }
                  });
          </script>
          """%message

        return HttpResponse(reponse)

class Registration(View):
    
    def get(self, request):

        return redirect("welcom")
    
    def post(self,request):
        message=""
        pseudo=request.POST['pseudo']
        photo=request.FILES['photo']
        password=request.POST['password']
        confirm_pass=request.POST['confirm-pass']
        #check user informations
        if len(pseudo) >= 4 and len(pseudo) <= 11:
          if re.match(r'^[a-z]', pseudo):
            if not User.objects.filter(username=pseudo).exists():
              if len(password) >= 6:
                if password == confirm_pass:
                  try:
                    date_naissance=date(int(request.POST['year']),int(request.POST['mounth']),int(request.POST['day']))
                    today=timezone.now().date()
                    age=today.year-date_naissance.year
                    #si l'anniversaire est deja passee
                    if(today.month,today.day) < (date_naissance.month,date_naissance.day):
                      age-=1
                    if age >= 18:
                      #valider l'inscription
                      try:
                        user=User.objects.create_user(username=pseudo, password=password)
                        data={
                          "user":user,
                          "photo":redimensioner_image(photo,400,400),
                          "dateNaissance":date_naissance,
                        }
                        profile=UserProfile(**data)
                        profile.save()
                        message='<i class="fas fa-check text-success"></i> Felicitations compte creer avec succes, vous pouvez maintenant vous <a href="">Connecter</a>'
                      except Exception as exc2:
                        print(exc2)
                        message=f'<i class="fas fa-exclamation-triangle text-danger"></i> Ops!!! une erreur inconnu, restez calme!'
                    else:
                      message='<i class="fas fa-exclamation-triangle text-danger"></i> Vous devez avoir 18 ans et plus pour rejoindre le chat'
                  except Exception as exc:
                    message='<i class="fas fa-exclamation-triangle text-danger"></i> Les donnees correspondant a votre date de naissance sont erronee, veuillez saisir des donnee valide'
                else:
                  message='<i class="fas fa-exclamation-triangle text-danger"></i> Mot de passe et confirm pass doivent etre identique'
              else:
                message='<i class="fas fa-exclamation-triangle text-danger"></i> Longeur mot de passe inferieur a 5'
            else:
              message='<i class="fas fa-exclamation-triangle text-danger"></i> Un utilisateur avec ce pseudo existe deja,veuillez en choisir un autre!'
  
          else:
            message='<i class="fas fa-exclamation-triangle text-danger"></i> Le pseudo ne doit pas commencer par une lettre majuscule ni un chiffre ni un caractere special'
        else:
          message='<i class="fas fa-exclamation-triangle text-danger"></i> Pseudo trop court, longeur autoriser entre 4 et 11 caracteres'
        
        reponse="""
        <script>
            Swal.fire({
                  title: 'Info!',
                  html:'%s',
                  confirmButtonText:'Ok, je vois',
                  showClass: {
                    popup: `
                      animate__animated
                      animate__fadeInUp
                      animate__faster
                    `
                  },
                  hideClass: {
                    popup: `
                      animate__animated
                      animate__fadeOutDown
                      animate__faster
                    `
                  }
                });
        </script>
        """%message
        return HttpResponse(reponse)

class HomePage(LoginRequiredMixin, View):

  def get(self, request):

    return render(request, "profile.html")


def deconnexion(request):
  logout(request)
  return redirect("welcom")
