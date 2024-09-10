from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import Http404
import datetime
from .forms import Signup, Login, SongEditForm
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Playlist, Song
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# 务必先激活source venv/bin/activate，再使用python3.9开头的命令如：python3.9 manage.py runserver
# 数据在about初始化，必须先访问about

def home(request):
    # retrieve data：modelObject = modelName.objects.all()
    playlists = Playlist.objects.all()
    return render(request,'zing_it/home.html',{"my_playlists":playlists})




def about(request):
    # create new songs and playlists using method: objectname.objects.create()
    try:

        car_playlist = Playlist.objects.create(name="Car Playlist",numberOfSongs=4)
        coding_playlist = Playlist.objects.create(name="Coding Playlist",numberOfSongs=2)

        thankyou_next= Song.objects.create(track="thank u, next",artist="Ariana Grande",album="thank u, next",length="3:27")
        one_kiss_next= Song.objects.create(track="One Kiss, next",artist="Dua Lipa, Calvin Harris",album="One Kiss",length="3:34")
        better_now= Song.objects.create(track="Better Now",artist="Post malone",album="beerbongs & bentleys",length="3:51")
        the_middle= Song.objects.create(track="The Middle",artist="Grey,Marren Morris, ZEDD",album="The Middle",length="3:04")
        love_lies= Song.objects.create(track="Love Lies",artist="Normani, Khalid",album="Love Lies",length="3:21")
        rise= Song.objects.create(track="Rise",artist="Jack & Jack, Jonas Blue",album="Blue",length="3:14")

        thankyou_next.save()
        one_kiss_next.save()
        better_now.save()
        the_middle.save()
        love_lies.save()
        rise.save()
        car_playlist.save()
        coding_playlist.save()

        # 设置manytomany关系, 使用 add() 方法将 Playlist 实例添加到 Song 实例的 ManyToManyField 中
        car_playlist.songs.add(thankyou_next)
        car_playlist.songs.add(one_kiss_next)
        car_playlist.songs.add(better_now)
        car_playlist.songs.add(the_middle)
        coding_playlist.songs.add(love_lies)
        coding_playlist.songs.add(rise)


        thankyou_next.save()
        one_kiss_next.save()
        better_now.save()
        the_middle.save()
        love_lies.save()
        rise.save()
        car_playlist.save()
        coding_playlist.save()

    except Exception as e: 
        print(e)
    return HttpResponse("welcome to zing_it")
    # return HttpResponse("""<h1>About Us:</h1><p>With Zing, you can easily find the music of your choice and easily share it with other people. You can also browse through the collections of friends, artists, and celebrities, or create a playlist of your own.
    #   Soundtrack your life with Zing. Subscribe or listen for free.</p>""")

# using database to restore user info
@login_required
def playlist(request, id):
    playlist_name = ""
    playlist = Playlist.objects.get(pk=id)      # pk=primary key，用主键获取对应的object，也可以用其他属性作为参数，但是只能返回唯一对象
    playlist_name = playlist.name
    if len(playlist_name)==0:                   # 判断是否存在这个playlist
        raise Http404("Such playlist does not exist")
    # 获取数据库的song，匹配当前playlist，Modelname.objects.filter(属性)
    # songs = Song.objects.filter(playlist_name__id=id)           # 等号左边是playlist_name是Song的属性__id表示过滤id与Playlist对象相同的id，等号右边的id是Playlist对象的id
    songs = playlist.songs.all()                              # 直接用反向关系查找，这个和上面那个都是可以的
    # if len(songs)!=0:
    #     print("have songs")
    #     for song in songs:
    #         print(song)
    # else:
    #     print("no song")
    return render(request, 'zing_it/songs.html', {"songs":songs, "playlist_name":playlist_name})
    

# edit song
def edit(request, id):
    # id是数据库里的song的id，获取数据库对象然后再根据用户的输入更改
    form = SongEditForm(request.POST or None)
    # 如果form有效，获取用户的输入数据
    if form.is_valid():
        # 用户输入的内容
        track = form.cleaned_data.get("track")
        artist = form.cleaned_data.get("artist")
        album = form.cleaned_data.get("album")
        length = form.cleaned_data.get("length")
        playlist_name = form.cleaned_data.get("playlist_name")
        # 获取数据库对应id的song并保存
        song = Song.objects.get(id=id)
        song.track = track
        song.artist = artist
        song.album = album
        song.length = length
        song.playlist_name = playlist_name
        song.save()
        return render(request, 'zing_it/edit.html', {"form":form, "status":"Your song is updated successfully!" })

    return render(request, 'zing_it/edit.html', {"form":form})




# using database to restore user info
def signup(request):
    # form去获取用户填写的数据，一开始是空的，传入空表让用户填写，用post返回，然后第二次从post返回的数据初始化表格，提取数据
    # 用User类来操作：user = User.objects.get()、new_user = User.objects.create_user(), new_user.save()
    form = Signup(request.POST or None)
    status = " "
    if form.is_valid():
        # 获取用户输入
        name = form.cleaned_data.get("full_name")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        confirm_password = form.cleaned_data.get("confirm_password")
        # 验证输入的密码是否两次一致
        if password != confirm_password:
            return render(request, 'zing_it/signup.html', {"form":form, "status":"Your passwords don't match!"})
        else:
            try:
                # 用用户输入的email在数据库查询是否有当前user
                user = User.objects.get(username=name, email=email)
                # 若存在， raise email already exists
                if user:
                    return render(request, 'zing_it/signup.html', {"form":form, "status":"This email already exists in the system! Please log in instead."})
            except Exception as e:
                print(e)
                # get方法查找不到会throw error， 在此处新建user，并保存到数据库
                new_user = User.objects.create_user(username=name, email=email, password=password)
                new_user.save()
                messages.success(request, "Registration successful. Please log in.")
                return redirect('login')  # 注册成功后重定向到登录页面
                # return render(request, 'zing_it/signup.html', {"form":form, "status": "Signed up Successfully!"})
    # 对应处理第一次请求的空表状态
    return render(request, 'zing_it/signup.html', {"form": form})


# using database to restore user info
# using authenticate to check the credentials 
def login(request):
    # form去获取用户填写的数据，一开始是空的，传入空表让用户填写，用post返回，然后第二次从post返回的数据初始化表格，提取数据
    form = Login(request.POST or None)
    status = " "
    if form.is_valid():
        # 获取用户的输入信息
        name = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = auth.authenticate(username=name, password=password)      # auth.authenticate(username,password)和数据库交互验证login信息
        if user:
            status = "Login successfully!"                              # 同时user.is_authenticate也变成True，更新给template
            auth.login(request, user)
            return redirect('home')                                   # auth.login(request, user)方法记录user的login信息到数据库
        else:
            status = "Wrong Credentials!"
    return render(request, 'zing_it/login.html', {"form":form, "status":status})


# 检查登录状态
def check_login_status(request):
    if request.user.is_authenticated:
        return JsonResponse({'redirect': None})  # User is logged in
    else:
        return JsonResponse({'redirect': '/login/'})  # Redirect to login page



# using dic to restore user info
def login1(request):
    # form去获取用户填写的数据，一开始是空的，传入空表让用户填写，用post返回，然后第二次从post返回的数据初始化表格，提取数据
    # next(生成器对象, default)
    form = Login(request.POST or None)
    status = " "
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        # 输入user与既有的user匹配
        user = next((user for user in users if user["email"]==email and user["password"]==password), None)
        if user:
            status = "Login successfully!"
        else:
            status = "Wrong Credentials!"
    return render(request, 'zing_it/login.html', {"form":form, "status":status})

# using dic to restore user info
def signup1(request):
    # form去获取用户填写的数据，一开始是空的，传入空表让用户填写，用post返回，然后第二次从post返回的数据初始化表格，提取数据
    form = Signup(request.POST or None)
    status = " "
    if form.is_valid():
        password = form.cleaned_data.get("password")
        confirm_password = form.cleaned_data.get("confirm_password")
        if password==confirm_password:
            status = "Sign up successfully!"
        else:
            status = "Sign up Failed!"
    return render(request, 'zing_it/signup.html', {"form":form, "status":status})

# using dic to restore user info
# def playlist1(request,id):
#     songs=[]
#     playlist_name=''
#     for playlist in my_playlists:
#         if(id == playlist['id']):
#             playlist_name=playlist['name']

#     if len(playlist_name)==0:
#         raise Http404("Such playlist does not exist")

#     for song in my_songs:
#         if(id == song['playlist_id']):
#             songs.append(song)
    
#     return render(request,'zing_it/songs.html',{"songs":songs,"playlist_name": playlist_name})



users = [
            {"id": 1, "full_name": "john", "email": "john123@gmail.com", "password": "adminpass"},
        ]

my_playlists=[
        {"id":1,"name":"Car Playlist","numberOfSongs":4},
        {"id":2,"name":"Coding Playlist","numberOfSongs":2}
    ]


# my_songs = [
#             {"id": 1, "Track": "thank u, next", "Artist": "Ariana Grande", "Album": "thank u, next", "Length": "3:27","playlist_id": 1},
#             {"id": 2, "Track": "One Kiss, next", "Artist": "Dua Lipa, Calvin Harris", "Album": "One Kiss", "Length": "3:34","playlist_id": 1},
#             {"id": 3, "Track": "Better Now", "Artist": "Post Malone", "Album": "beerbongs & bentleys", "Length": "3:51","playlist_id": 1},
#             {"id": 4, "Track": "The Middle", "Artist": "Grey,Marren Morris, ZEDD", "Album": "The Middle", "Length": "3:04","playlist_id": 1},
#             {"id": 5, "Track": "Love Lies", "Artist": "Normani, Khalid", "Album": "Love Lies", "Length": "3:21","playlist_id": 2},
#             {"id": 6, "Track": "Rise", "Artist": "Jack & Jack, Jonas Blue", "Album": "Blue", "Length": "3:14","playlist_id": 2},
#     ]


