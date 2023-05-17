import requests
import json
import time
import streamlit as st

endpoint = 'https://api-eu.restb.ai/vision/v2/multipredict'


def get_data_from_image(image_url):
    api_methods = ['caption', 're_features_v4', 're_roomtype_international', 're_condition_r1r6_global']
    image_data = {}
    for api_solution in api_methods:
        payload = {
            # Add the client key to the parameters dictionary
            "client_key": st.secrets["client_key"],
            "model_id": api_solution,
            "image_url": image_url
        }
        headers = {
            "X-Client-ID": st.secrets["X_Client_ID"],
            "X-Property-ID": st.secrets["X_Property_ID"]
        }

        response = requests.get(endpoint, params=payload, headers=headers)
        data = response.json()
        image_data[api_solution] = data
        time.sleep(3)

    return image_data


# with open('data.json', 'w', encoding='utf-8') as f:
# json.dump(image_data, f, ensure_ascii=False, indent=4)


def get_attributes_from_data(image_data):
    try:
        caption = ''
        if image_data['caption'].get('error') == 'false':
            caption = image_data['caption'].get('response').get('solutions').get('caption').get('description')
    except:
        caption = None
    try:
        features = []
        if image_data['re_features_v4'].get('error' == 'false'):
            for detection in image_data['re_features_v4'].get('detections'):
                features.append(detection.get('label'))
    except:
        features = None
    try:
        room_type = ''
        if image_data['re_roomtype_international'].get('error') == 'false':
            room_type = image_data['re_roomtype_international'].get('response').get('solutions').get(
                're_roomtype_international').get('top_prediction').get('label')
    except:
        room_type = None
    try:
        score = 0
        if image_data['re_condition_r1r6_global'].get('error') == 'false':
            score = image_data['re_condition_r1r6_global'].get('response').get('solutions').get(
                're_condition_r1r6_global').get('score')
    except:
        score = None

    info_features = {
        'caption': caption,
        'features': features,
        'room_type': room_type,
        'score': score
    }

    return info_features


def create_estate_description(image_urls):
    list_recomendations = ["idealista", "fotocasa","airbnb","Apartaments.com","Homes & Villas by Marriott","VOB | Luxary Property Managment"]
    caption_description = "This house offers"
    counter_score = 0
    score = 0
    for image_url in image_urls:
        caption_description += " a "
        data = get_data_from_image(image_url)
        info_photo = get_attributes_from_data(data)
        caption_description +=  info_photo.get('caption') + ","
        if info_photo.get('score'):
            score += 7-info_photo.get('score')
            counter_score += 1
    caption_description = caption_description.rstrip(caption_description[-1])+"."
    recomendation = str(list_recomendations[round(score/counter_score)])
    score = (score/counter_score)*10/6
    socre_description = " The approximate score of the house is "+str(round(score, 2))
    return caption_description+socre_description, recomendation


