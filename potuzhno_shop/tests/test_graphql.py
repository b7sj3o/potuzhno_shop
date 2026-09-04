import pytest
from django.urls import reverse
from rest_framework import status

from apps.shop.models import Category, Brand, Product


def test_product_list_ok(api_client, product):
    query = """
    query {
        allProducts { id name }
    }
    """

    response = api_client.get("/graphql/", {"query": query}, format="json")

    assert response.status_code == 200
    assert response.json()["data"]["allProducts"][0]["name"] == "Худі Oversize"

