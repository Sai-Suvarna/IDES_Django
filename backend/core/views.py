# core/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from core.serializers import WordSerializer
from core.serializers import ImageSerializer
from core.serializers import ImageSerializer1

from core.serializers import ProductDetailsSerializer
from core.models import ProductDetails

from core.models import Word, Image
import requests

from rest_framework.decorators import api_view
from .models import ProductDetails

import uuid
import PIL.Image
import os
import google.generativeai as genai


import tempfile 
from PIL import Image

UPLOAD_FOLDER = 'static'


# Function to configure the Google API key
def configure_google_api(api_key):
    genai.configure(api_key=api_key)


# Load the environment variables
# Configure the Google API key
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY environment variable not set")
configure_google_api(api_key)


# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
UPLOAD_FOLDER = 'static'

model = genai.GenerativeModel('gemini-1.5-flash')

def fetch_from_knowledge_graph(query):
    # api_key = GOOGLE_API_KEY
    api_endpoint = "https://kgsearch.googleapis.com/v1/entities:search"
    params = {
        "query": query,
        "key": api_key
    }
    response = requests.get(api_endpoint, params=params)
    data = response.json()
    return data

def display_knowledge_graph_data(data, query, upimage):
    results = []
    unique_names = set()  # Maintain a set of unique names
    
    if "itemListElement" in data:
        for item in data["itemListElement"]:
            name = item["result"]["name"]
            if name.lower() == query.lower() and name not in unique_names:  # Check if the name is unique
                item_image = item["result"].get("image", {}).get("contentUrl", "No image available")
                if item_image != "No image available":
                    description = item["result"].get("detailedDescription", {}).get("articleBody", "No detailed description available")
                    detailed_description = item["result"].get("detailedDescription", {}).get("url", "No detailed description available")
                    result_dict = {
                        "Name": name,
                        "Description": description,
                        "Detailed Description": detailed_description,
                        "item_image": item_image
                    }
                    results.append(result_dict)
                    unique_names.add(name)
                else:
                    model1 = genai.GenerativeModel('gemini-pro')
                    query="Give me a description of 60 words about" + name
                    response = model1.generate_content(query)
                    description=response.text
                    detailed_description = item["result"].get("detailedDescription", {}).get("url", "No detailed description available")
                    item_image=upimage
                    result_dict = {
                        "Name": name,
                        "Description": description,
                        "Detailed Description": detailed_description,
                        "item_image": item_image
                    }
                    results.append(result_dict)
    
                    unique_names.add(name)
    print(unique_names)
    return results



def display_knowledge_graph_data1(data, query):
    results = []
    unique_names = set()  # Maintain a set of unique names
    
    if "itemListElement" in data:
        for item in data["itemListElement"]:
            name = item["result"]["name"]
            if name.lower() == query.lower() and name not in unique_names:  # Check if the name is unique
                item_image = item["result"].get("image", {}).get("contentUrl", "No image available")
                description = item["result"].get("detailedDescription", {}).get("articleBody", "No detailed description available")
                detailed_description_url = item["result"].get("detailedDescription", {}).get("url")

                # If no detailed description available, generate Wikipedia link
                if not detailed_description_url:
                    wikipedia_url = f"https://en.wikipedia.org/wiki/{name}"
                    detailed_description = f"{wikipedia_url}"
                else:
                    detailed_description = detailed_description_url

                # If no description available, generate one using Generative AI
                if description == "No detailed description available":
                    model1 = genai.GenerativeModel('gemini-pro')
                    query_description = "Give me a description of 60 words about " + name
                    response = model1.generate_content(query_description)
                    description = response.text

                result_dict = {
                    "Name": name,
                    "Description": description,
                    "Detailed Description": detailed_description,
                    "item_image": item_image
                }
                results.append(result_dict)
                unique_names.add(name)
    
    return results

##### ---  API call for input word without database ---####

# class ProcessWordView(APIView):
#     parser_classes = [JSONParser]  # Add JSONParser to handle JSON input

#     def get(self, request, *args, **kwargs):
#         return Response({"message": "Please use POST method to submit a word."}, status=status.HTTP_200_OK)

#     def post(self, request, *args, **kwargs):
#         serializer = WordSerializer(data=request.data)
#         if serializer.is_valid():
#             word_instance = serializer.save()
#             search_word = word_instance.word
#             object_results = []

#             # Fetch data from the knowledge graph
#             data = fetch_from_knowledge_graph(search_word)
#             object_data = display_knowledge_graph_data1(data, search_word)
#             object_results.extend(object_data)

#             return Response({"object_results": object_results}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#### --- API call for input word with database --- ####

class ProcessWordView(APIView):
    parser_classes = [JSONParser]  # Add JSONParser to handle JSON input

    def get(self, request, *args, **kwargs):
        serializer = WordSerializer(data=request.data)
        if serializer.is_valid():
            word_instance = serializer.save()
            search_word = word_instance.word
            object_results = []

            # Fetch data from the knowledge graph
            data = fetch_from_knowledge_graph(search_word)
            object_data = display_knowledge_graph_data1(data, search_word)
            object_results.extend(object_data)

            # Fetch matching items from the database
            matching_products = []
            products = ProductDetails.objects.filter(item__icontains=search_word)
            for product in products:
                matching_products.append({
                    'productId': product.productId,
                    'category': product.category,
                    'item': product.item,
                    'description': product.description,
                    'units': product.units,
                    'thresholdValue': product.thresholdValue,
                    'image': product.image
                })

            return Response({
                #"object_results": object_results,
                "matching_products": matching_products
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



##### ---  API call for image upload without database ---####

# class UploadImageView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

    # def post(self, request):
    #     image_file = request.FILES.get('image')
    #     if image_file:
    #         filename = str(uuid.uuid4()) + os.path.splitext(image_file.name)[-1]
    #         save_path = os.path.join(UPLOAD_FOLDER, filename)

    #         if not os.path.exists(UPLOAD_FOLDER):
    #             os.makedirs(UPLOAD_FOLDER)

    #         with open(save_path, "wb") as image:
    #             for chunk in image_file.chunks():
    #                 image.write(chunk)

    #         img = PIL.Image.open(save_path)

    #         # Your image processing code here
    #         response = model.generate_content(["""Identify the only some important things that are in the image.If any machinery parts, hardware tools, or components are detected, provide their specific names of each object without any stopwords
    #         . I should have the response only consist of names of all the objects name in a single word for each one without any stopwords in the object names separated by comma in the image""", img], stream=True)            

    #         response.resolve()

    #         res = response.text.split(',')
    #         res = [word.strip() for word in res if word.strip()]

    #         object_results = []
    #         for obj in res:
    #             data = fetch_from_knowledge_graph(obj)
    #             object_data = display_knowledge_graph_data(data, obj, save_path)
    #             object_results.extend(object_data)

    #         # Save the recognized words to the database
    #         for word in res:
    #             Word.objects.create(word=word)

    #         return Response({
    #             "res": res,
    #             "object_results": object_results,
    #         }, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response({"error": "No image provided."}, status=status.HTTP_400_BAD_REQUEST)

##### ---  API call for image upload with database ---####

class UploadImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        image_file = request.FILES.get('image')
        if image_file:
            filename = str(uuid.uuid4()) + os.path.splitext(image_file.name)[-1]
            save_path = os.path.join(UPLOAD_FOLDER, filename)

            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            with open(save_path, "wb") as image:
                for chunk in image_file.chunks():
                    image.write(chunk)

            img = PIL.Image.open(save_path)

            # Your image processing code here
            response = model.generate_content([
                """Identify the only some important things that are in the image.
                If any machinery parts, hardware tools, or components are detected, 
                provide their specific names of each object without any stopwords.
                I should have the response only consist of names of all the objects 
                name in a single word for each one without any stopwords in the object names separated by comma in the image""",
                img
            ], stream=True)

            response.resolve()

            res = response.text.split(',')
            res = [word.strip() for word in res if word.strip()]

            object_results = []
            for obj in res:
                data = fetch_from_knowledge_graph(obj)
                object_data = display_knowledge_graph_data(data, obj, save_path)
                object_results.extend(object_data)

            # Fetch matching items from the database
            matching_products = []
            for obj in res:
                products = ProductDetails.objects.filter(item__icontains=obj)
                for product in products:
                    matching_products.append({
                        'productId': product.productId,
                        'category': product.category,
                        'item': product.item,
                        'description': product.description,
                        'units': product.units,
                        'thresholdValue': product.thresholdValue,
                        'image': product.image
                    })

            return Response({
                "res": res,
                #"object_results": object_results,
                "matching_products": matching_products,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "No image provided."}, status=status.HTTP_400_BAD_REQUEST)




   
#### ----- API call to get matching details of the input word throught get method ----- ####

@api_view(['GET'])
def get_product_details(request, input_word):
    # Query the database to retrieve all rows where the item column matches the input word
    matching_products = ProductDetails.objects.filter(item__icontains=input_word)
    
    # Serialize the query results
    serialized_products = []
    for product in matching_products:
        serialized_product = {
            'productId': product.productId,
            'category': product.category,
            'item': product.item,
            'description': product.description,
            'units': product.units,
            'thresholdValue': product.thresholdValue,
            'image': product.image,
        }
        serialized_products.append(serialized_product)
    
    return Response({'matching_products': serialized_products})




#### ---- API call to get results form the image taken from camera --- ####

class WebcamImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        print(request.FILES)
        if not request.FILES:
           print("No files submitted.")
           return JsonResponse({'errors': {'image': 'No image file submitted'}}, status=status.HTTP_400_BAD_REQUEST)
        
        image_file = request.FILES.get('image')
        print (image_file.name)
        image_path = os.path.join(UPLOAD_FOLDER, 'captured_image.jpg')

        # Save the image to a file
        with open(image_path, 'wb') as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        # Open the image using PIL
        img = PIL.Image.open(image_path)

        # Your image processing code here
        response = model.generate_content(["Identify the only some important things that are in the image.I should have the response only consist of names of all the objects name in a single word for each one without any stopwords in the object names separated by comma in the image ", img], stream=True)
        response.resolve()

        res = response.text.split(',')
        res = [word.strip() for word in res if word.strip()]

        object_results = []
        for obj in res:
            data = fetch_from_knowledge_graph(obj)
            object_data = display_knowledge_graph_data(data, obj, image_path)
            object_results.extend(object_data)

        return JsonResponse({
            "res": res,
            "object_results": object_results,
        })



### ----- API call for retrieving details from the table --- ####
from rest_framework import generics
class ProductDetailsList(generics.ListAPIView):
    queryset = ProductDetails.objects.all()
    serializer_class = ProductDetailsSerializer



