import pytest
from fastapi import HTTPException
from http import HTTPStatus
from app.api.products.services import ProductService
from asyncmock import AsyncMock
from app.api.products.models import Product
from app.api.bakeries.models import Bakery


@pytest.fixture
def product_service():
    return ProductService()


@pytest.mark.asyncio
async def test_list_products(product_service):
    # Test case: List Products
    limit = 10
    offset = 0
    name = "Cake"
    location = "New York"
    product_service.product_dao.filter = AsyncMock(
        return_value=[Product(id=1, name="Cake", price=9.99, location="New York")])
    result = await product_service.list_products(
        limit=limit, offset=offset, name=name, location=location)

    assert isinstance(result, list)
    assert len(result) == 1


@pytest.mark.asyncio
async def test_delete_product(product_service):
    # Test case: Delete Product
    product_id = 123
    user_id = 456

    # Case: No orders associated with the product
    product_service.order_dao.filter = AsyncMock(return_value=[])
    product_service.bakery_dao.get_bakery_by_owner_id = AsyncMock(
        return_value=Bakery(id=789))
    product_service.product_dao.delete_product_model = AsyncMock()

    result = await product_service.delete_product(product_id, user_id)

    assert result == {'success': True, 'message': 'Product deleted successfully'}

    # Case: Orders associated with the product
    product_service.order_dao.filter = AsyncMock(return_value=[{"id": 111}])

    with pytest.raises(HTTPException) as exc:
        await product_service.delete_product(product_id, user_id)

    assert exc.value.status_code == HTTPStatus.BAD_REQUEST
    assert exc.value.detail == 'Cannot delete product with orders'


@pytest.mark.asyncio
async def test_update_product(product_service):
    # Test case: Update Product
    product_id = 123
    payload = {'name': 'New Cake', 'price': 9.99}
    user_id = 456

    # Case: Product exists and belongs to the user
    product_service.bakery_dao.get_bakery_by_owner_id = AsyncMock(
        return_value=Bakery(id=789))
    product_service.product_dao.filter = AsyncMock(
        return_value=[Product(id=product_id, baker_id=789)])
    product_service.product_dao.update_product_model = AsyncMock()

    result = await product_service.update_product(product_id, payload, user_id)

    assert result == {'success': True, 'message': 'Product updated successfully'}

    # Case: Product does not exist or does not belong to the user
    product_service.product_dao.filter = AsyncMock(return_value=[])

    with pytest.raises(HTTPException) as exc:
        await product_service.update_product(product_id, payload, user_id)

    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == 'Product not found'
