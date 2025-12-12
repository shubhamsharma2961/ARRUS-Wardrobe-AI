from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Wardrobe, Occasion
from .serializers import WardrobeSerializer, RegisterSerializer, LoginSerializer
from api.ai_model import extract_features, suggest_outfit_based_on_features
import random
import traceback

'''class CustomTokenObtainView(APIView):
    def post(self, request):
        try:
            serializer = CustomTokenObtainSerializer(data=request.data)
            if serializer.is_valid():
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            return Response({
                'data':{},
                'message':'something went wrong'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)'''

class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data= request.data)
        if serializer .is_valid():
            serializer.save()
            return Response({"message":"User Registered successfully."},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self,request):
        serializer= LoginSerializer(data= request.data)
        if serializer .is_valid():
            return Response({
                "refresh_token":serializer.validated_data['refresh_token'],
                "access_token":serializer.validated_data['access_token']
            },status=status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def ai_model_suggest_outfit(wardrobe_items, occasion):
        try:
            return random.sample(wardrobe_items, min(3, len(wardrobe_items)))
        except Exception as e:
            traceback.print_exc()
            return Response({
                'data':{},
                'message':'something went wrong'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class UploadWardrobe(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            wardrobe_items= Wardrobe.objects.filter(user= request.user)
            serializer= WardrobeSerializer(wardrobe_items, many= True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response({
                'data':{},
                'message':'something went wrong'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = WardrobeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            return Response({
                'data':{},
                'message':'something went wrong, cannot save.'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self,request, id=None):
        try:
            wardrobe_item= Wardrobe.objects.get(id=id)
            serializer= WardrobeSerializer(wardrobe_item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status= status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Wardrobe.DoesNotExist:
            return Response({
                'data':{},
                'message':'wardrobe item not found'
            },status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            traceback.print_exc()
            return Response({
                'data':{},
                'message':'something went wrong, cannot update.'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, id=None):
        try:
            wardrobe_item=Wardrobe.objects.get(id=id)
            wardrobe_item.delete()
            return Response({
                'data':{},
                'message':'Wardrobe item deleted successfully.'
            },status=status.HTTP_204_NO_CONTENT)
        except Wardrobe.DoesNotExist:
            return Response({
                'data':{},
                'message':'Wardrobe item not found.'
            },status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            traceback.print_exc()
            return Response({
                'data':{},
                'message':'something went wrong, cannot delete.'
            })
     
class SuggestOutfitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        occasion_name = request.data.get('occasion')
        formality= request.data.get('formality')
        if not occasion_name:
            return Response({"error": "Occasion is required"}, status=400)
        try:
            occasion = get_object_or_404(Occasion, name=occasion_name)
        except Occasion.DoesNotExist:
            return Response({'error': 'Invalid occasion'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            return Response({
                'data':{},
                'message':'something went wrong'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        user_wardrobe = Wardrobe.objects.filter(user=request.user, formality= formality)
        wardrobe_items = list(user_wardrobe)

        if not wardrobe_items:
            return Response({'error': 'Wardrobe is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        #occasion_features= np.random.rand(1,1280)   

        suggested_outfits = suggest_outfit_based_on_features(wardrobe_items, occasion_name)

        if not suggested_outfits:
            print(f"No suitable outfits found for occasion {occasion_name}")
            return Response({'error':'no suitable outfits found'},status= status.HTTP_400_BAD_REQUEST)
                    
        serialized_outfits = []
        for outfit in suggested_outfits:
            serialized_outfits.append({
                'top': WardrobeSerializer(outfit['top']).data,
                'bottom': WardrobeSerializer(outfit['bottom']).data,
                'shoes': WardrobeSerializer(outfit['shoes']).data
            })

        return Response({'outfits': serialized_outfits}, status=status.HTTP_200_OK)


'''class SuggestOutfitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        occasion_id = request.data.get('occasion')
        try:
            occasion = Occasion.objects.get(id=occasion_id)
        except Occasion.DoesNotExist:
            return Response({'error': 'Invalid occasion'}, status=status.HTTP_400_BAD_REQUEST)

        user_wardrobe = Wardrobe.objects.filter(user=request.user)
        wardrobe_items = list(user_wardrobe)

        if not wardrobe_items:
            return Response({'error': 'Wardrobe is empty'}, status=status.HTTP_400_BAD_REQUEST)

        occasion_features = np.random.rand(1, 1280)

        suggested_outfit = suggest_outfit_based_on_features(wardrobe_items, occasion_features)
        if not suggested_outfit:
            return Response({'error': 'No suitable outfit found'}, status=status.HTTP_404_NOT_FOUND)

        suggestion_serializer = WardrobeSerializer(suggested_outfit, many=True)
        
        return Response({'outfit': suggestion_serializer.data}, status=status.HTTP_200_OK)
'''