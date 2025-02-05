"""
# certificatin/views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from google.cloud import vision
import requests
import pandas as pd
import os
from django.contrib.auth.decorators import login_required
import json
from django.utils.translation import activate
from django.contrib.auth import login as auth_login

# 環境変数でサービスアカウントのパスを指定
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/y_ooba/Desktop/venv/vision-travel-project-448601-c4ca0fa7e25b.json"

# 楽天APIの設定
PLACES_API_KEY = "AIzaSyCaJee3wWa3zhI4Lumrg7qMFOKos4Ki_3g"
APP_ID = "1030179497105717784"  # 楽天APIのAPP_ID
REQUEST_URL = "https://app.rakuten.co.jp/services/api/Travel/SimpleHotelSearch/20170426"

def mainmenu_view(request):
    return render(request, 'certification/mainmenu.html')

def upload(request):
    return render(request, 'certification/upload.html')  # upload.htmlをレンダリング

def history(request):
    return render(request, 'certification/history.html')

def settings_view(request):
    return render(request, 'certification/settings.html')


@csrf_exempt
def upload_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        fs = FileSystemStorage()
        saved_file_path = fs.save(image.name, image)
        saved_file_url = fs.url(saved_file_path)
        file_full_path = fs.path(saved_file_path)

        # Google Vision APIを使用して画像を解析
        client = vision.ImageAnnotatorClient()
        with open(file_full_path, "rb") as image_file:
            content = image_file.read()
        image_vision = vision.Image(content=content)
        response = client.landmark_detection(image=image_vision)
        landmarks = response.landmark_annotations

        # ランドマークデータを整形
        results = []
        latitude = None
        longitude = None
        if landmarks:
            for landmark in landmarks:
                name = landmark.description
                lat = landmark.locations[0].lat_lng.latitude
                lon = landmark.locations[0].lat_lng.longitude
                results.append({
                    "name": name,
                    "latitude": lat,
                    "longitude": lon,
                })

                # 最初のランドマークの緯度経度を取得
                if latitude is None and longitude is None:
                    latitude = lat
                    longitude = lon

        # 楽天APIでホテル情報を取得
        hotel_links = rakuten_api(latitude, longitude)

        # 全ホテル情報をJSONファイルに保存
        json_file_path = os.path.join("C:/Users/y_ooba/Desktop/venv/visiontravel", "hotel_links.json")
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(hotel_links, json_file, ensure_ascii=False, indent=4)

        # ランドマーク情報とホテルリンクのデータをresult.htmlに渡す
        return render(request, "certification/result.html", {
            "landmarks": results,
            "file_url": saved_file_url,  # アップロードされた画像のURL
            "hotel_links": hotel_links  # ホテルリンクのデータ
        })

    return render(request, "certification/upload.html")


@login_required
def mainmenu_views(request):
    user = request.user
    language_code = "ja" if user.language_code == 1 else "en"  # ← 1ならja, 2ならen
 
    print(f"現在のユーザー: {user.user_name}, 言語コード: {language_code}")  # デバッグ
 
    return render(request, 'certification/mainmenu.html', {
        "user_name": user.user_name,
        "language_code": language_code
    })


def rakuten_api(latitude, longitude):
    filtered_data = []

    for page in range(1, 16):    
        params = {
            "format": "json",
            "latitude": latitude,
            "longitude": longitude,
            "searchRadius": 2,
            "datumType": 1,
            "applicationId": APP_ID,
            "page": page
        }
        res = requests.get(REQUEST_URL, params)
        result = res.json()
        hotels = result.get("hotels", [])

        for hotel in hotels:
            hotel_info = hotel["hotel"][0]["hotelBasicInfo"]
            filtered_info = {
                "hotelName": normalize_string(hotel_info.get("hotelName")),
                "hotelInformationUrl": hotel_info.get("hotelInformationUrl")
            }
            filtered_data.append(filtered_info)

    return filtered_data


import re
import unicodedata

def normalize_string(s):
    if not s:
        return ""
    # 全角・半角統一、トリム、カタカナ化
    s = unicodedata.normalize("NFKC", s).strip().lower()
    s = re.sub(r"[\(\[].*?[\)\]]", "", s)  # 括弧や角括弧内の文字を削除
    s = re.sub(r"\s+", " ", s)  # 余分なスペースを削除
    s = s.replace("旅館", "").replace("そのまま", "ソノママ")  # 固有ルールを適用
    return s

from difflib import SequenceMatcher

def find_best_match(hotel_name, hotel_links):
    from difflib import SequenceMatcher

    def similarity(a, b):
        return SequenceMatcher(None, a, b).ratio()

    normalized_name = normalize_string(hotel_name)
    best_match = None
    max_score = 0

    for hotel in hotel_links:
        normalized_hotel_name = normalize_string(hotel["hotelName"])
        score = similarity(normalized_name, normalized_hotel_name)
        if score > max_score:
            max_score = score
            best_match = hotel

    if max_score >= 0.7:  # 類似度のしきい値を下げる
        return best_match
    return None



def load_hotel_links():
    json_file_path = os.path.join("C:/Users/y_ooba/Desktop/venv/visiontravel", "hotel_links.json")
    if os.path.exists(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            hotel_links = json.load(json_file)
        return hotel_links
    return []  # ファイルがない場合、空のリストを返す

# 他のビューでload_hotel_linksを使用する例
def get_hotel_links(request):
    hotel_links = load_hotel_links()
    return JsonResponse(hotel_links, safe=False)
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from google.cloud import vision
from django.contrib.auth.decorators import login_required
import os
from django.http import JsonResponse
import requests
import pandas as pd
import os
import json
import re
import unicodedata
from difflib import SequenceMatcher
from django.utils.translation import activate
from django.contrib.auth import login as auth_login
 
# Google Cloud Vision API のクライアントを設定
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/y_ooba/Desktop/venv/vision-travel-project-448601-c4ca0fa7e25b.json"
 
# 楽天APIの設定
PLACES_API_KEY = "AIzaSyCaJee3wWa3zhI4Lumrg7qMFOKos4Ki_3g"
APP_ID = "1030179497105717784"  # 楽天APIのAPP_ID
REQUEST_URL = "https://app.rakuten.co.jp/services/api/Travel/SimpleHotelSearch/20170426"
 
def login_view(request):
    if request.method == 'POST':
        # ログイン処理
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth_login(request, user)
            # 言語をセッションに保存して適用
            request.session['django_language'] = user.language_code
            activate(user.language_code)
            return redirect('mainmenu')  # ホーム画面へリダイレクト
    return render(request, 'login.html')
 
@csrf_exempt
def upload_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        # ユーザーの言語設定を取得
        user = request.user
        language_code = "ja" if user.language_code == 1 else "en"
 
        # 画像を保存
        image = request.FILES["image"]
        fs = FileSystemStorage()
        saved_file_path = fs.save(image.name, image)
        saved_file_url = fs.url(saved_file_path)
        file_full_path = fs.path(saved_file_path)
 
        # Google Vision APIで画像解析
        client = vision.ImageAnnotatorClient()
        with open(file_full_path, "rb") as image_file:
            content = image_file.read()
        image_vision = vision.Image(content=content)
        response = client.landmark_detection(image=image_vision)
        landmarks = response.landmark_annotations
 
        # ランドマークデータを整形
        results = []
        latitude = longitude = None
        if landmarks:
            for landmark in landmarks:
                name = landmark.description
                lat = landmark.locations[0].lat_lng.latitude
                lon = landmark.locations[0].lat_lng.longitude
                results.append({
                    "name": name,
                    "latitude": lat,
                    "longitude": lon,
                })
                if latitude is None and longitude is None:
                    latitude, longitude = lat, lon
 
        # 楽天APIでホテル情報を取得
        hotel_links = []
        if latitude is not None and longitude is not None:
            hotel_links = rakuten_api(latitude, longitude)
            json_file_path = os.path.join("C:/Users/y_ooba/Desktop/venv/visiontravel", "hotel_links.json")
            with open(json_file_path, "w", encoding="utf-8") as json_file:
                json.dump(hotel_links, json_file, ensure_ascii=False, indent=4)
 
        # `result.html` にデータを渡す
        return render(request, "certification/result.html", {
            "landmarks": results,
            "file_url": saved_file_url,
            "hotel_links": hotel_links,
            "language_code": language_code,
        })
   
    return render(request, "certification/upload.html")
 
@login_required
def mainmenu_views(request):
    user = request.user
    language_code = "ja" if user.language_code == 1 else "en"  # ← 1ならja, 2ならen
 
    print(f"現在のユーザー: {user.user_name}, 言語コード: {language_code}")  # デバッグ
 
    return render(request, 'certification/mainmenu.html', {
        "user_name": user.user_name,
        "language_code": language_code
    })
 
def rakuten_api(latitude, longitude):
    """楽天APIでホテル情報を取得し、ホテル名とURLの辞書を返す"""
    filtered_data = []
 
    for page in range(1, 16):    
        params = {
            "format": "json",
            "latitude": latitude,
            "longitude": longitude,
            "searchRadius": 2,
            "datumType": 1,
            "applicationId": APP_ID,
            "page": page
        }
        res = requests.get(REQUEST_URL, params)
        result = res.json()
        hotels = result.get("hotels", [])
 
        for hotel in hotels:
            hotel_info = hotel["hotel"][0]["hotelBasicInfo"]
            filtered_info = {
                "hotelName": normalize_string(hotel_info.get("hotelName")),
                "hotelInformationUrl": hotel_info.get("hotelInformationUrl")
            }
            filtered_data.append(filtered_info)
 
    return filtered_data
 
 
def normalize_string(s):
    """文字列を正規化し、比較のために統一する"""
    if not s:
        return ""
    # 全角・半角統一、トリム、カタカナ化
    s = unicodedata.normalize("NFKC", s).strip().lower()
    s = re.sub(r"[\(\[].*?[\)\]]", "", s)  # 括弧や角括弧内の文字を削除
    s = re.sub(r"\s+", " ", s)  # 余分なスペースを削除
    s = s.replace("旅館", "").replace("そのまま", "ソノママ")  # 固有ルールを適用
    return s
 
def find_best_match(hotel_name, hotel_links):
    """ホテル名に最も一致するリンクを探す"""
    from difflib import SequenceMatcher
 
    def similarity(a, b):
        return SequenceMatcher(None, a, b).ratio()
 
    normalized_name = normalize_string(hotel_name)
    best_match = None
    max_score = 0
 
    for hotel in hotel_links:
        normalized_hotel_name = normalize_string(hotel["hotelName"])
        score = similarity(normalized_name, normalized_hotel_name)
        if score > max_score:
            max_score = score
            best_match = hotel
 
    if max_score >= 0.7:  # 類似度のしきい値を下げる
        return best_match
    return None
 
def load_hotel_links():
    """保存されたJSONファイルからホテルリンクを読み込む"""
    json_file_path = os.path.join("C:/Users/y_ooba/Desktop/venv/visiontravel", "hotel_links.json")
    if os.path.exists(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            hotel_links = json.load(json_file)
        return hotel_links
    return []  # ファイルがない場合、空のリストを返す
 
# 他のビューでload_hotel_linksを使用する例
def get_hotel_links(request):
    hotel_links = load_hotel_links()
    return JsonResponse(hotel_links, safe=False)