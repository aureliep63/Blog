from django.shortcuts import render
from listings.models import Blog
from listings.forms import BlogForm
from django.shortcuts import redirect


def blog_list(request):
        # on prend tous les objects de la table Band
    blog = Blog.objects.all()
        # on retourne la requete, route de la page hello, table band
    return render(request, 'listings/blog_list.html', {'blog': blog})

def blog_detail(request, id):
        # get permet de retourner un seul objet
        # get(id=id) veut dire 'obtenez moi l'objet qui a cet id'
    blog =  Blog.objects.get(id=id) 
    return render(request, 'listings/blog_detail.html', {'blog': blog})

def blog_add(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            # créer une nouvelle « Blog » et la sauvegarder dans la db
            blog = form.save()
            # redirige vers la page de détail du groupe que nous venons de créer
            # nous pouvons fournir les arguments du motif url comme arguments à la fonction de redirection
            return redirect('blog-list')
    else:
        form = BlogForm()
    return render(request,
            'listings/blog_add.html',
            {'form': form})


def blog_update(request, id):
    blog = Blog.objects.get(id=id) # get car un récupère un seul élément
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog) # on prérempli le formulaire avec un groupe existant grace a instance
        if form.is_valid(): # mettre à jour le groupe existant ds la base de données
            form.save()
            return redirect('blog-detail', blog.id)
    else:
        form = BlogForm(instance=blog)
    return render(request, 'listings/blog_update.html', {'form': form})


def blog_delete(request, id):
    blog = Blog.objects.get(id=id)  

    if request.method == "POST":
        # supprimer le groupe de la base de données
        blog.delete()
        # rediriger vers la liste des groupes
        return redirect('blog-list')

    # pas besoin de « else » ici. Si c'est une demande GET, continuez simplement
    return render(request,
                    'listings/blog_delete.html',
                    {'blog': blog})