from re import findall
from typing import Dict
from bs4 import BeautifulSoup

def parse_text(text):
    text = text.replace("\n"," ")
    text = " ".join(text.split())
    return text


def parse_date(text : str):
    remove_text = "Reviewed in the United States on"
    text =  text.replace(remove_text,"")
    return text.strip()


def parse_helpful_count(text : str):
    edge_cases = {"One person found this helpful" : 1}
    for key, val in edge_cases.items():
        if key == text:
            return edge_cases[key]
    return int(findall(pattern=r"\d+", string=text)[0])


def parse_rating(text : str):
    remove_text = "out of 5 stars"
    text = text.replace(remove_text, "")
    text = text.strip()
    return float(text)


def parse_images(image_tag : BeautifulSoup):
    image_tag = image_tag.find_all(attrs={"src" : True})
    image_urls = []
    for tag in image_tag:
        image_urls.append(tag["src"])
    return image_urls
    
    
def parse_review(review : Dict):
    """Parse Amazon's review."""
    content = {}
    for heading, body in review.items():

        if heading == "title":
            body = parse_text(body)

        if heading == "date":
            body = parse_date(body)

        if heading == "helpful_count":
            if body is not None:
                body = parse_helpful_count(body.text)
            else:
                body = 0

        if heading == "rating":
            if body is not None:
                body = parse_rating(body)
            else:
                body = 0.0

        if heading == "body":
            if body is not None:
                body = parse_text(body.text)
            else:
                body = ""

        if heading == "images":
            if body is not None:
                body = parse_images(body)
            else:
                body = []
                
        content[heading] = body 
    return content