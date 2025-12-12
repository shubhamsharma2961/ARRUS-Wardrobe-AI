import tensorflow as tf 
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np
import random
import os 

model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')

def load_and_preprocess_image(img_path):
    img= image.load_img(img_path, target_size=(224,224))
    img_array= image.img_to_array(img)
    img_array= np.expand_dims(img_array, axis=0)
    img_array= preprocess_input(img_array)
    return img_array

def extract_features(image_path):
    image_array= load_and_preprocess_image(image_path)
    features= model.predict(image_array)
    return features

def suggest_outfit_based_on_features(wardrobe_items, occasion_name):
    print(f"Received wardrobe_items: {wardrobe_items}, occasion_name: {occasion_name}")
    if occasion_name == "formal":
        suggested_outfits= [
            item for item in wardrobe_items if item.formality =="formal"
        ]
    elif occasion_name == "casual":
        suggested_outfits= [
            item for item in wardrobe_items if item.formality =="casual"
        ]
    elif occasion_name == "sports":
        suggested_outfits= [
            item for item in wardrobe_items if item.formality =="sports"
        ]
    elif occasion_name == "party":
        suggested_outfits= [
            item for item in wardrobe_items if item.formality =="party"
        ]
    else:
        return suggested_outfits
    
    suggested_outfits= []
    for item in wardrobe_items:
        print(f"Category:{item.category}, formality:{item.formality}")
        if occasion_name == "formal" and item.formality == "formal":
            suggested_outfits.append(item)
    print(f"suggested outfits:{suggested_outfits}") 

    tops = [item for item in wardrobe_items if item.category.lower() in ['top', 'shirt', 't-shirt','kurta']]
    bottoms = [item for item in wardrobe_items if item.category.lower() in ['pant', 'jeans', 'shorts','trousers','skirt']]
    shoes = [item for item in wardrobe_items if item.category.lower() in ['shoes', 'sneakers','crocs','slippers','boots']]
    
    if not tops or not bottoms or not shoes:
        return []

    outfit_combinations = []        
    for _ in range(3):
        top = random.choice(tops)
        bottom = random.choice(bottoms)
        shoe = random.choice(shoes)
        outfit_combinations.append({
            'top': top,
            'bottom': bottom,
            'shoes': shoe
        })
    return outfit_combinations



    '''if np.any(features):  
        if occasion == 'casual':
            return "Jeans and T-Shirt"
        elif occasion == 'formal':
            return "Suit and Tie"
        elif occasion == 'party':
            return "Fancy Dress"
    else:
        return None'''
    
    '''if np.any(features) and occasion == 'casual':
        return "Jeans and T-Shirt"
        elif np.any(features) and occasion == 'formal':
            return "Suit and Tie"
        elif np.any(features) and occasion == 'party':
            return "Fancy Dress"
        else:
            return No suitable outfit found for the given occasion.'''
    
    '''outfit_suggestions = {
            'casual': ['Jeans and T-shirt', 'Sneakers', 'Cap'],
            'formal': ['Suit and tie', 'Dress shoes', 'Watch'],
            'party': ['Blazer', 'Chinos', 'Loafers'],
            'sport': ['Tracksuit', 'Running shoes', 'Headband'],
        }

        if occasion in outfit_suggestions:
            return random.choice(outfit_suggestions[occasion])
        else:
            raise ValueError("Invalid occasion")'''

    '''def suggest_outfit_based_on_features(wardrobe_items, occasion_features):
        suggested_items = []
        for item in wardrobe_items:
            item_features = extract_features(item.image.path)
            similarity = np.dot(item_features, occasion_features.T)
            if similarity > 0.8:
                suggested_items.append(item)
    
        return suggested_items'''

