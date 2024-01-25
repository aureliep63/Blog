# Création d'une petite application web

###### *Exercice DJANGO afin d'ajouter, de modifier, de supprimer et d'afficher des articles de blogs*


## Création du project Blog

Se positionner dans le dossier voulu pour le project.
Dans la ligne de commande:
Création du project:

```bash
django-admin startprojct blog
```
Vérifier être dans le bon dossier en tapant:
```bash
ls
```
-> blog/ manage.py
Activer le project:
```bash
python manage.py runserver
```

Dans son IDE, ouvrir le dossier Blog
    blog/
        manage.py
        blog/
            __init__.py
            settings.py
            urls.py
            asgi.py
            wsgi.py

Ouvrir le terminal:
Créer listings qui hébergera l'application
```bash	
python manage.py startapp listings 
```	
Vous devriez avoir
    listings/
        __init__.py
        admin.py
        apps.py
        migrations/
            __init__.py
        models.py
        tests.py
        views.py

### Configurer la base de données
Avec Django vous avez automatiquement Sqlite
Pour configurer une base de données MySql:
Dans la base de données, créer une table que vous appelerez dans 'NAME'
Dans Blog/blog/settings.py
```python	
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME':'nom du project dans la bdd',
            'USER': 'nom du user de la bdd',
            'PASSWORD': 'mdp de la bdd',
            'HOST': 'host bdd',
            'PORT': 'port de la bdd',
        }
    }
```

### Intégrer l'application
Toujours dans settings.py
Ajouter l'application listing dans INSTALLED_APPS
```python	
INSTALLED_APPS = [
    'django.contrib.admin',
    '...',
    'listings',
    ]
```

### Créer un model et l'insérer dans la base de donnée
Dans Blog/blog/listings/models.py
```python
from django.db import models

class Blog(models.Model):

    class Tags(models.TextChoices):
        PYTHON = 'py'
        PHP = 'php'
        LANGAGE = 'lg'
        POLITIQUE = 'pol'
        SPORT = 'sp'

    titre = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, null=True)
    photo = models.CharField(max_length=255, null=True)
    tag=models.CharField(choices=Tags.choices, max_length=10, null=True)
```

Bien faire attention à l'indentation

Il faut créer la class Blog qui est dans models
On choisi le nom de la colonne, qui est égal dans le model au type avec des contraintes entre ()
ex: titre comme nom de colonne
    pour le type:   - CharlField pour les chaines de caractère
                    - IntegerField pour les nombres
                    - TextField pour le texte
                    - URLField pour les urls
                    - ...
    pour les contraintes:   - max_length pour le nombre de caractère max
                            - null = True pour possibilité de case vide
                            - choices = Tags.choices pour les choix multiples
    pour les choix multiples, il faut créer en amont une class avec les valeurs qui seront affichés et les valeurs insérées dans la bdd



### Envoyer les données à la base de données
```bash
python manage.py makemigrations
```
si tout est ok
```bash
python manage.py migration
```


### Création du portail Admin
Les admins on la possibilité de créer, modifier, ajouter ou même supprimer via ce portail
Pour le créer:
```bash
python manage.py createsuperuser
```
renseigner à la suite un identifiant, un mail et un mot de passe
(le mot de passe ne s'affiche pas pas mesure de sécurité)
Suivre le lien et se connecter 

Vous pouvez modifer l'affichage dans de vos colonnes dans le portail
Dans Blog/blog/listings/admin.py
```python
# toujours importer les pages nécessaires
from django.contrib import admin
from listings.models import Blog

class BlogAdmin(admin.ModelAdmin):
    # indiquer à la suite tous les champs voulus ('titre','...','...')
    list_display = ('titre')
admin.site.register(Blog)
```
### Activation de l'infrastructure du site
Dans Blog/blog/listings/settings.py
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    '...',
    'django.contrib.sites', 
]

SITE_ID = 1
```

### Création des views et des urls et templates

#### Les Urls

```python
# Toujours importer les pages nécessaire
from django.contrib import admin
from django.urls import path
from listings import views

#ici nous auront les routes avec le nom des views.pagesHtml correspondantes et les noms voulus qu'on reprendra dans les passerelles des views
urlpatterns = [
    # ici pour la page admin
    path('admin/', admin.site.urls),
    path('blog/', views.blog_list, name='blog-list'),
    path('blog/<int:id>/', views.blog_detail, name='blog-detail'),
    path('blog/<int:id>/update/', views.blog_update, name='blog-update'),
    path('blog/add', views.blog_add, name='blog-add'),
    path('blog/<int:id>/delete/', views.blog_delete, name='blog-delete'),
]
```

#### Les views
```python 
# on importe les pages nécessaire
from django.shortcuts import render
from listings.models import Blog
from listings.forms import BlogForm
# Pour le redirect, il faudra insérer des données dans le settings
from django.shortcuts import redirect
```

Dans Blog/blog/listings/settings.py
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    '...', 
    'django.contrib.redirects',
]
```

Dans Blog/blog/listings/views.py
Faire une méthode pour chaque tâches

###### Pour afficher la liste des articles
```python
def blog_list(request):
        # on prend tous les objects de la table Band
    blog = Blog.objects.all()
        # on retourne la requete, route de la page hello, table band
    return render(request, 'listings/blog_list.html', {'blog': blog})
```

###### Pour ajouter des articles
D'abord créer un formulaire dans Blog/blog/listings/forms.py
```python
# on importe les pages nécessaires
from django import forms
from listings.models import Blog

# faire une class Form avec les champs qu'il y a dans Blog et tous les retourner
class BlogForm(forms.ModelForm):
   class Meta:
        model = Blog
        fields= '__all__'
```
Dans Blog/blog/listings/views.py
```python
def blog_add(request):
    # si la requete est en methode POST, soit qu'elle se trouvera dans le corps 
    if request.method == 'POST':
        # on récupère le formulaire
        form = BlogForm(request.POST)
        # si le formulaire est valide
        if form.is_valid():
            # créer une nouvelle ligne de « Blog » et la sauvegarder dans la bdd
            blog = form.save()
            # redirige vers la page où tous les articles sont affichés du groupe que nous venons de créer
            return redirect('blog-list')
            # sinon on reste sur le formulaire
    else:
        form = BlogForm()
    return render(request,
            'listings/blog_add.html',
            {'form': form})
```


###### Pour afficher un article en détail 
```python
def blog_detail(request, id):
        # get permet de retourner un seul objet
        # get(id=id) veut dire 'obtenez moi l'objet qui a cet id'
    blog =  Blog.objects.get(id=id) 
    return render(request, 'listings/blog_detail.html', {'blog': blog})
```

###### Pour modifier des articles

Ne pas oublier de faire des liens pour pouvoir modifier
```html	
<a href="{% url  'blog-update' blog.id %}" class="ms-4"> Modifier cet article</a>
```

```python
def blog_update(request, id):
    blog = Blog.objects.get(id=id) # get car un récupère un seul élément
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog) 
        # on prérempli le formulaire avec un groupe existant grace a instance
        if form.is_valid(): 
            # si le formulaire est valide
            # mettre à jour le groupe existant ds la base de données
            form.save()
            #on redirige vers le détail de l'article
            return redirect('blog-detail', blog.id)
    else:
        # sinon on reste sur cette page avec le formulaire prérempli
        form = BlogForm(instance=blog)
    return render(request, 'listings/blog_update.html', {'form': form})
```

###### Pour modifier des articles
Ne pas oublier de faire des liens pour supprimer
```HTML
<a href="{% url 'blog-delete' blog.id %}">Supprimer</a>
```

```PYTHON
def blog_delete(request, id):
    blog = Blog.objects.get(id=id)  

    if request.method == "POST":
        # supprimer le groupe de la base de données
        blog.delete()
        # rediriger vers la liste des groupes
        return redirect('blog-list')

    # pas besoin de « else » 
    return render(request,
                    'listings/blog_delete.html',
                    {'blog': blog})

```


##### Les templates
Créer des pages html voulus, soit dans ce cas:
Dans Blog/blog/listings/templates/listings
<!-- création d'une base -->
    base.html
<!-- Création de la page pour afficher tous nos articles  -->
    blog_list.html
<!-- Création de la page du formulaire d'ajout -->
    blog_add.html
<!-- Création de page de détails des articles -->
    blog_detail.html
<!-- Création de la page de modification des articles -->
    blog_edit.html
<!-- Création de la page de suppression des articles -->
    blog_delete.html

Dans la base, importer le css, scripts souhaités, nav et footer et autres éléments qui se répercutera sur toutes les pages du site

Sur toutes les pages hors base.html
Il faut extends base.html pour que les propriétés s'étendent
{% extends "listings/base.html" %}

Pour la page d'affichage des articles, faire une boucle FOR  pour afficher tous les articles de la table Blog
```HTML
{% for blog in blog %}
<h5>{{ blog.titre }}</h5>
<p>{{ blog.description  }}</p>
{% endfor %}
```

Styliser au choix, ici le style est fait avec Boostrap

Si on écrit <p>{{ blog.tag  }}</p>, sera affiché la valeur écrit dans la bdd
Il faut écrire <p>{{ blog.get_tag_display }}</p>

Pour les formulaires d'ajout et de modification:
```html
<form action="" method="POST" class="text-center">
    <!-- pour échapper aux attaques -->
    {% csrf_token %}
    <!-- form permet de récupérer tous les éléments du formulaire directement -->
    {{ form.as_p }}
    <input type="submit" value="Envoyer">
</form>

```

Pour la suppression, il est mieux de demander la confirmation de suppression

Quelques soit la page, bien mettre des liens pour revenir sur les pages précédentes et la page d'acccueil
<a href="{% url 'blog-list' %}" class="ms-4">Revenir aux articles</a>





