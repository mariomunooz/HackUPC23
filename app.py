import streamlit as st
from PIL import Image
from io import BytesIO
from Imgur import generate_url as gu
import json
import os
import requests
from streamlit_lottie import st_lottie
import time

from api_interaction import api_main as apim

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    return img

marketplaces = {"idealista": 'https://media.licdn.com/dms/image/C4E0BAQFT8QKTQ2nSRQ/company-logo_200_200/0/1657530226563?e=1692230400&v=beta&t=yCq4Is1bnlJEJ-YIAUi2m_L3S6clyVnFfSir-2iRrFM',
                "fotocasa": 'https://media.licdn.com/dms/image/C4D0BAQFY3JkVqCf4qw/company-logo_200_200/0/1647258551462?e=1692230400&v=beta&t=8pP7nJbNwlgis9Lej2o_YP9SODyu-IKWK4uIqoaEgrk',
                "airbnb": 'https://media.licdn.com/dms/image/C560BAQFhfl32crIGIw/company-logo_200_200/0/1595528954632?e=1692230400&v=beta&t=CoR0a6qMBPibqMFwpR1-P2wTw8BwJRu12qSwBbfLR-A',
                "Apartaments.com": 'https://media.licdn.com/dms/image/C4D0BAQHy4UIAeM4b2Q/company-logo_200_200/0/1611080558976?e=1692230400&v=beta&t=JwMvlwZ5ig0ZckfDo3N798gCF_aewlKN096VWUHPiq8',
                "Homes & Villas by Marriott": 'https://media.licdn.com/dms/image/D560BAQFDl770EloMlw/company-logo_200_200/0/1664986548204?e=1692230400&v=beta&t=VsHFCQmqPDWPoluDi2tnKp-s1DzvV3kiK3FU4L_aMlc',
                "VOB | Luxary Property Managment": "https://media.licdn.com/dms/image/C560BAQHMYil-Sj6a8w/company-logo_200_200/0/1582801122554?e=2147483647&v=beta&t=UNR8iHvr9Esa3mLOS4TC3uZBzaqcCv6BDO9KA1kj7Y8"}


marketplaces_and_d = {
    "idealista": """Idealista is a prominent Spanish real estate platform, offering an extensive range of properties 
    for sale and rent. Founded in 2000, it has become one of the most recognized portals for buying and renting 
    properties in Spain. Idealista has over 1.7 million active listings, and its platform attracts millions of 
    visitors every month. With more than 20 years of experience in the industry, Idealista has established itself as 
    a trusted source for real estate information and has helped millions of people find their dream homes in Spain.""",
    "fotocasa": """Fotocasa is the leading property portal in Spain, featuring 1.5 million second-hand properties, 
    new home developments, and rental opportunities. Founded in 1999, the portal has 20 years’ experience in helping 
    millions of people find homes around Spain.""",
    "airbnb":"""Airbnb was born in 2007 when two Hosts welcomed three guests to their San Francisco home, 
    and has since grown to over 4 million Hosts who have welcomed 1.4 billion guest arrivals in almost every country 
    across the globe. Every day, Hosts offer unique stays and experiences that make it possible for guests to connect 
    with communities in a more authentic way.""",
    "Apartaments.com":"""Powered by CoStar, the Apartments.com network reaches millions of renters nationwide, 
    driving both qualified traffic and highly engaged renters to leasing offices. Whether you’re a property manager, 
    multifamily marketer, or independent landlord, our suite of online tools allows you to fully showcase your 
    community, promote your reputation and manage your property.""",
    "Homes & Villas by Marriott": """Homes & Villas by Marriott Bonvoy offer a curated and growing collection of 
    premium and luxury whole home rentals located in prime destinations throughout the world.

Leveraging Marriott International’s deep knowledge in delivering exceptional hospitality experiences, each home is 
professionally managed and meets the company’s design, cleanliness, safety and amenity standards.

Homes & Villas by Marriott Bonvoy is part of the Marriott Bonvoy travel program, providing numerous benefits to both 
property management companies and travelers. Members of Marriott Bonvoy can earn and redeem points at all homes, 
providing more choice for a range of travel needs as a complement to Marriott International’s core hotel business.""",
    "VOB | Luxary Property Managment": """VDB Luxury Properties is a boutique luxury agency. We work for discerning 
    clients who look for best-in-class, highly personalized property management services, property rental, 
    and sales. We strive to be the only boutique service of this kind!"""
}


# set the title of the web app
st.title("Real State Marketplace Recommender")

# display some text in the app
st.write("""Do you want to rent your house, but you're not sure where to start? We're here to help! Our team of 
experts can guide you through the process and help you find the perfect tenant for your property. Whether you're a 
first-time landlord or an experienced property owner, we have the knowledge and expertise to make the rental process 
as smooth and stress-free as possible. """)

st.write("""\n\n\nWe make renting out your property easy! With our streamlined process, we only need the images of your 
house to get started. You can relax and let us take care of the rest. Our team of experts will use advanced image 
recognition technology to analyze the visual features of your property, and provide personalized recommendations 
based on those features. """)

st.write("""\n\n**Upload 4 Images of your house**""")
# Create a button for users to upload photos
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])


number_of_images_stored = gu.get_num_of_images_stored()


# Display the uploaded photo
if uploaded_file is not None:
    img = uploaded_file.read()

    image_url = gu.uploadToBlobStorage2(img, os.path.splitext(uploaded_file.name)[-1] )


while number_of_images_stored < 3:
    time.sleep(1)


st_lottie( load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_lp7qD9RDx1.json"), height=200, )


st.write("**House Description**")

house_description, recommended_market = apim.create_estate_description(gu.get_urls_of_images_stored())

st.write(house_description)

st.write("**RECOMENDED REAL STATE MARKETPLACE**")





left_column, right_column = st.columns([3, 7])

# Add content to the left column
with left_column:
    st.image(load_image(marketplaces[recommended_market]),
             caption=recommended_market)

# Add content to the right column
with right_column:
    st.write(marketplaces_and_d[recommended_market])







